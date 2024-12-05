#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include "rthread.h"

#define WHISTLER 0
#define LISTENER 1
struct device
{
    	rthread_sema_t mutex;
	rthread_sema_t w_sema;
	rthread_sema_t l_sema;

	int nw_inside, nw_waiting;
	int nl_inside, nl_waiting;
};

void dev_vacateOne(struct device *dev);
void dev_init(struct device *dev);
void dev_enter(struct device *dev, int which);
void dev_exit(struct device *dev, int which);

void dev_vacateOne(struct device *dev) {
	// If there are no WHISTLERS in the CS and there are LISTENERS waiting,
	// release one of the waiting LISTENERS.
	if (dev->nw_inside == 0 && dev->nl_waiting > 0) {
		dev->nl_waiting--;
		rthread_sema_vacate(&dev->l_sema);
	}
	
	// If there are no LISTENERS in the CS and there are WHISTLERS waiting,
	// release one of the waiting WHISTLERS.
	if (dev->nl_inside == 0 && dev->nw_waiting > 0) {
		dev->nw_waiting--;
		rthread_sema_vacate(&dev->w_sema);
	}

	// Otherwise, stop protecting shared variables.
	else {
		rthread_sema_vacate(&dev->mutex);
	}
}

void dev_init(struct device *dev) {
	rthread_sema_init(&dev->mutex, 1);
	rthread_sema_init(&dev->w_sema, 0);
	rthread_sema_init(&dev->l_sema, 0);
	dev->nw_inside = dev->nw_waiting = 0;
	dev->nl_inside = dev->nl_waiting = 0;
}

void dev_enter(struct device *dev, int which) {
	if (which) {	// Enter for WHISTLER
		rthread_sema_procure(&dev->mutex);
	
		// If there are LISTENERS inside, wait
		if (dev->nl_inside > 0) {
			dev->nw_waiting++;
			dev_vacateOne(dev);
			rthread_sema_procure(&dev->w_sema);
		}
		assert(dev->nl_inside == 0);
		
		dev->nw_inside++;
		assert(dev->nw_inside > 0);
		dev_vacateOne(dev);
	}
	else {		// Enter for LISTENER
		rthread_sema_procure(&dev->mutex);
		
		// If there are WHISTLERS inside, wait
		if (dev->nw_inside > 0) {
			dev->nl_waiting++;
			dev_vacateOne(dev);
			rthread_sema_procure(&dev->l_sema);
		}
		assert(dev->nw_inside == 0);
		
		dev->nl_inside++;
		assert(dev->nl_inside > 0);
		dev_vacateOne(dev);
	
	}
}

void dev_exit(struct device *dev, int which) {
	if (which) {	// Exit for WHISTLER
		rthread_sema_procure(&dev->mutex);
    	assert( ( dev->nl_inside == 0 ) && ( dev->nw_inside > 0 ) );
    	dev->nw_inside--;
    	dev_vacateOne(dev);
	}
	else {		// Exit for LISTENER
		rthread_sema_procure(&dev->mutex);
		assert( ( dev->nw_inside == 0 ) && ( dev->nl_inside > 0 ) );
    	dev->nl_inside--;
    	dev_vacateOne(dev);
	}
}

// =============================================================
//          Test Code for Lab of Ornithology IoT Device
// =============================================================

#define NWHISTLERS 3
#define NLISTENERS 3
#define NEXPERIMENTS 2

char *whistlers[NWHISTLERS] = {"w1", "w2", "w3"};
char *listeners[NLISTENERS] = {"l1", "l2", "l3"};

void worker(void *shared, void *arg)
{
    struct device *dev = shared;
    char *name = arg;
    for (int i = 0; i < NEXPERIMENTS; i++)
    {
        printf("worker %s waiting for device\n", name);
        dev_enter(dev, name[0] == 'w');
        printf("worker %s has device\n", name);
        rthread_delay(random() % 3000);
        printf("worker %s releases device\n", name);
        dev_exit(dev, name[0] == 'w');
        rthread_delay(random() % 3000);
    }
    printf("worker %s is done\n", name);
}

int main()
{
    struct device dev;
    dev_init(&dev);
    for (int i = 0; i < NWHISTLERS; i++)
    {
        rthread_create(worker, &dev, whistlers[i]);
    }
    for (int i = 0; i < NLISTENERS; i++)
    {
        rthread_create(worker, &dev, listeners[i]);
    }
    rthread_run();
    return 0;
}
