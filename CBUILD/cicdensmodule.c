#include "Python.h"

#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>


static PyObject *cicdens_calcd_cic(PyObject *, PyObject *);
static PyObject *cicdens_calcd_zel(PyObject *, PyObject *);

int pmap_cell(long long int, double, int, int *, double *, double *);

static PyMethodDef dMethods[] = {
    {"calcd_cic",	cicdens_calcd_cic,			METH_VARARGS, "calcd_cic"},
    {"calcd_zel",	cicdens_calcd_zel,			METH_VARARGS, "calcd_zel"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};


PyMODINIT_FUNC initcicdens(void)
{
    PyObject *m;

    m = Py_InitModule("cicdens", dMethods);
    if (m == NULL)
        return;
  //  import_array();
    
}




int pmap_cell(long long int i,double fact, int nparticles, int *cell, double *posincell, double *pos) {
	
	long long int nsq=nparticles*nparticles;
	long long int x=i/nsq;
	i=i-x*nsq;
	long long int y=i/nparticles;
	i=i-y*nparticles;
	long long int z=i;
	

	

	pos[0]=((double)x)*fact;
	pos[1]=((double)y)*fact;
	pos[2]=((double)z)*fact;

	
	cell[0]= (int)(pos[0]+0.5);
	cell[1]= (int)(pos[1]+0.5);
	cell[2]= (int)(pos[2]+0.5);	

	
	posincell[0]=pos[0] - (double)cell[0];
	posincell[1]=pos[1] - (double)cell[1];
	posincell[2]=pos[2] - (double)cell[2];
	return 0;
	
}


static PyObject *cicdens_calcd_zel(PyObject *self, PyObject *args)
{
	int ngrid;
	double boxlen;
	double growthrate;
	long long int xfp, yfp, zfp;
	long long int fptr, dptr;
	double *xf, *yf, *zf;
	long long int nparticles;

	if (!PyArg_ParseTuple(args, "iLddLLLL", &ngrid,  &nparticles, &boxlen, &growthrate, &xfp, &yfp, &zfp, &dptr))
        	return NULL;
	xf=(double *)xfp;
	yf=(double *)yfp;
	zf=(double *)zfp;
	
	double *density=(double *)dptr;
	double cell_len=((double)boxlen)/((double)ngrid);
	
	long long int i;
	int j;
	double dngx, dngy, dngz;
	int cell[3];
	int neighbor[3];
	double posincell[3];
	double pos[3];
	double np = rint((double) pow(nparticles, 1./3.));
	int npside = (int) np;
	double fact=((double) ngrid)/((double) npside);
	double f[3];
	
	for (i=0; i<nparticles; i++) {	
		
		pmap_cell(i, fact, npside,cell, posincell, pos);
		

		for (j=0; j<3; j++) {
			
			neighbor[j]=cell[j];
			if (posincell[j] >0)
				neighbor[j]+=1;
			else
				neighbor[j]-=1;
			
			if (neighbor[j] < 0)
				neighbor[j] = ngrid-1;
			if (neighbor[j] >= ngrid)
				neighbor[j]-=ngrid;
			if (cell[j] == ngrid)
				cell[j]=0;
			if (neighbor[j] >= ngrid || neighbor[j] < 0)
                ;
				//printf("1: uh oh out of bounds\n");
			if (cell[j] >=ngrid || cell[j] < 0)
                ;
				//printf("2: uh oh cell out of bounds\n");
			
		}
		
		
		
		dngx=fabs(posincell[0]);
		dngy=fabs(posincell[1]);
		dngz=fabs(posincell[2]);
		
		
		
		
		
		f[0]=(1-dngx)*xf[cell[2]+cell[1]*ngrid+cell[0]*ngrid*ngrid];
		f[0]+=(dngx)*xf[cell[2]+cell[1]*ngrid+neighbor[0]*ngrid*ngrid];
		
		f[1]=(1-dngy)*yf[cell[2]+cell[1]*ngrid+cell[0]*ngrid*ngrid];
		f[1]+=(dngy)*yf[cell[2]+neighbor[1]*ngrid+cell[0]*ngrid*ngrid];
		
		f[2]=(1-dngz)*zf[cell[2]+cell[1]*ngrid+cell[0]*ngrid*ngrid];
		f[2]+=(dngz)*zf[neighbor[2]+cell[1]*ngrid+cell[0]*ngrid*ngrid];
		

		
		
		f[0]*=(1.0+growthrate);
		
		for (j=0; j<3; j++) {
			f[j]+=pos[j]*cell_len;
			if (f[j] >= boxlen)
				f[j]-=boxlen;
			if (f[j] < 0)
				f[j] += boxlen;
			cell[j]=(int)(f[j]/cell_len+0.5);
			posincell[j]=f[j]/cell_len-(double)cell[j];
			neighbor[j]=cell[j];
			if (posincell[j] >0)
				neighbor[j]+=1;
			else
				neighbor[j]-=1;
			
			if (neighbor[j] < 0)
				neighbor[j] = ngrid-1;
			if (neighbor[j] >= ngrid)
				neighbor[j]-=ngrid;
			if (cell[j] == ngrid)
				cell[j]=0;
			if (neighbor[j] >= ngrid || neighbor[j] < 0)
                ;
				//printf("3: uh oh out of bounds\n");
			if (cell[j] >=ngrid || cell[j] < 0)
                ;
				//printf("4: uh oh cell out of bounds\n");
				
				
		}
		
		
		dngx=fabs(posincell[0]);
		dngy=fabs(posincell[1]);
		dngz=fabs(posincell[2]);
		
		
		density[cell[2] + ngrid * cell[1] + ngrid*ngrid* cell[0]]+=(1-dngx)*(1-dngy)*(1-dngz);
		density[neighbor[2] + ngrid * cell[1] + ngrid*ngrid *cell[0]]+=(1-dngx)*(1-dngy)*(dngz);
		density[neighbor[2]+ngrid*neighbor[1]+ngrid*ngrid *cell[0]]+=(1-dngx)*(dngy)*(dngz);
		density[neighbor[2]+ngrid*cell[1]+ngrid*ngrid*neighbor[0]]+=(dngx)*(1-dngy)*(dngz);
		density[neighbor[2]+ngrid*neighbor[1]+ngrid*ngrid*neighbor[0]]+=(dngx)*(dngy)*(dngz);
		density[cell[2]+ngrid*neighbor[1]+ngrid*ngrid*cell[0]]+=(1-dngx)*(dngy)*(1-dngz);
		density[cell[2]+ngrid*neighbor[1]+ngrid*ngrid*neighbor[0]]+=(dngx)*(dngy)*(1-dngz);
		density[cell[2]+ngrid*cell[1]+ngrid*ngrid*neighbor[0]]+=(dngx)*(1-dngy)*(1-dngz);
		 
		 
	}
	

 
 
	return Py_BuildValue("i", 1.0);

}

static PyObject *cicdens_calcd_cic(PyObject *self, PyObject *args)
{
    
	
	
	int ngrid;
	double boxlen;
	long long int xpptr;
	long long int ypptr;
	long long int zpptr;
	long long int dptr;
	double *xpos, *ypos, *zpos;
	int numparts;
    	if (!PyArg_ParseTuple(args, "iidLLLL", &ngrid,&numparts, &boxlen, &xpptr, &ypptr, &zpptr, &dptr))
        	return NULL;
	xpos=(double *)xpptr;
	ypos=(double *)ypptr;
	zpos=(double *)zpptr;
	double *density=(double *)dptr;
	
	
	double cell_len=(boxlen)/((double)ngrid);
	int i;
	int j;
	double dngx, dngy, dngz;
	int cell[3];
	int neighbor[3];
	double posincell[3];
	for (i=0; i<numparts; i++) {
		
		cell[0]=(int)(xpos[i]/cell_len+0.5);
		cell[1]=(int)(ypos[i]/cell_len+0.5);
		cell[2]=(int)(zpos[i]/cell_len+0.5);
		
		posincell[0]=xpos[i]/(cell_len) - (double)cell[0];
		posincell[1]=ypos[i]/(cell_len) - (double)cell[1];
		posincell[2]=zpos[i]/(cell_len) - (double)cell[2];
		
		for (j=0; j<3; j++) {
			neighbor[j]=cell[j];
			if (posincell[j] >0)
				neighbor[j]+=1;
			else
				neighbor[j]-=1;
			
			if (neighbor[j] < 0)
				neighbor[j] = ngrid-1;
			if (neighbor[j] >= ngrid)
				neighbor[j]-=ngrid;
			if (cell[j] >= ngrid)
				cell[j]-=ngrid;
			if (neighbor[j] >= ngrid || neighbor[j] < 0) {
				printf("uh oh out of bounds\n");
			}
			if (cell[j] >=ngrid || cell[j] < 0) {
				printf("uh oh cell out of bounds\n");
			}
			
		}
		dngx=fabs(posincell[0]);
		dngy=fabs(posincell[1]);
		dngz=fabs(posincell[2]);
		
		
		
		density[cell[2] + ngrid * cell[1] + ngrid*ngrid* cell[0]]+=(1-dngx)*(1-dngy)*(1-dngz);
		density[neighbor[2] + ngrid * cell[1] + ngrid*ngrid *cell[0]]+=(1-dngx)*(1-dngy)*(dngz);
		density[neighbor[2]+ngrid*neighbor[1]+ngrid*ngrid *cell[0]]+=(1-dngx)*(dngy)*(dngz);
		density[neighbor[2]+ngrid*cell[1]+ngrid*ngrid*neighbor[0]]+=(dngx)*(1-dngy)*(dngz);
		density[neighbor[2]+ngrid*neighbor[1]+ngrid*ngrid*neighbor[0]]+=(dngx)*(dngy)*(dngz);
		density[cell[2]+ngrid*neighbor[1]+ngrid*ngrid*cell[0]]+=(1-dngx)*(dngy)*(1-dngz);
		density[cell[2]+ngrid*neighbor[1]+ngrid*ngrid*neighbor[0]]+=(dngx)*(dngy)*(1-dngz);
		density[cell[2]+ngrid*cell[1]+ngrid*ngrid*neighbor[0]]+=(dngx)*(1-dngy)*(1-dngz);
        
        
		
	}
	
	return Py_BuildValue("i", 1.0);
}


int main(int argc, char *argv[])
{
    /* Pass argv[0] to the Python interpreter */
    Py_SetProgramName(argv[0]);

    /* Initialize the Python interpreter.  Required. */
    Py_Initialize();

    /* Add a static module */
    initcicdens();
    return 0;
}
