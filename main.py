import sys
import time
import math
import cairo
import logging
import numpy as np
import argparse
import IPython
from math import pi, radians
from os.path import exists

import cairo_utils as utils
from cairo_utils.dcel.constants import VertE, EdgeE, FaceE
import citygen

    

N = 12
SIZE = pow(2,N)
HALFSIZE = int(SIZE * 0.5)
SCALER = 1 / SIZE
TIME = 100
imgPath = "./imgs/"
imgName = "initialTest"
dcel_filename = "theDCEL"
currentTime = time.gmtime()
FONT_SIZE = SIZE / 30
SCALE = False
INC_AMNT = 15
SUBDIV = 10
RADIUS = 3

#Operators:
heightmap = citygen.HeightmapOperator(SIZE,SUBDIV, 0, 5, 3, RADIUS)
river = citygen.RiverOperator(100, octaves=2, deviance=0.15, repeats=None)
bezRiv = citygen.BezierRiverOperator(1, deviance=0.15)
roadOperator = citygen.RoadOperator([1,4], [1,4], amnt=50, hbal=0.5, hbounds=[600,1000])

#The City:
city = citygen.City(standard_rules=[],
                    specific_rules={citygen.RoadOperator : [citygen.IntersectionOperator()]})


#change to a stack/heap?
all_operators = [roadOperator]

#------------------------------
# def MAIN TICK
#------------------------------
def tick(dc, i):
    if not bool(all_operators):
         return True
    
    #select operator
    op = city.choose_operator(all_operators)
    #TODO: verify the op has an operate method
    
    with citygen.OperatorTemplate.setup_operator(op,dc, i, city=city):
        #place operator
        
        #parameterize operator

        #perform operation
        delta = op.operate(draw=True)

        #verify operation
        verify_result = city.verify(dc, i, delta, verify_type=type(op))
            

        if verify_result is citygen.verify_results.FAIL:
            raise Exception("Operator failed")

        #remove from pool?
        if op.is_oneshot():
            all_operators.remove(op)
    
    return False

def save(args, theDCEL):
    if not args.dontsave:
        logging.info("Saving DCEL")
        try:
            theDCEL.savefile(dcel_filename)
        except Exception as e:
            logging.exception(e)
            IPython.embed(simple_prompt=True)

def draw(args, theDCEL):
    if not args.dontdraw:
        final_name = "{}_FINAL".format(saveString)
        logging.info("Drawing to: {}".format(final_name))
        utils.dcel.drawing.drawDCEL(ctx, theDCEL, faces=True, edges=True, verts=True,
                                    background_colour=[0,0,0,1], text=True)
        utils.drawing.write_to_png(surface, final_name)



if __name__ == "__main__":
    #------------------------------
    # def ARG PARSER SETUP
    #------------------------------
    parser = argparse.ArgumentParser("")
    parser.add_argument('-l', "--loaddcel", action="store_true")
    parser.add_argument('--dontsave', action="store_true")
    parser.add_argument('-s', '--static', action="store_true")
    parser.add_argument('-d', '--dontdraw',action="store_true")
    parser.add_argument('--drawsteps', action="store_true")
    parser.add_argument('-n', '--numpoints',type=int, default=N)
    parser.add_argument('-t', '--timesteps', type=int, default=TIME)
    parser.add_argument('--ipython', action="store_true")
    args = parser.parse_args()
    
    #format the name of the image to be saved thusly:
    saveString = "{}{}_{}-{}_{}-{}".format(imgPath,
                                           imgName,
                                           currentTime.tm_min,
                                           currentTime.tm_hour,
                                           currentTime.tm_mday,
                                           currentTime.tm_mon,
                                           currentTime.tm_year)

    #------------------------------
    # def LOGGING SETUP
    #------------------------------

    LOGLEVEL = logging.DEBUG
    logFileName = "log.CityGen"
    logging.basicConfig(filename=logFileName,level=LOGLEVEL,filemode='w')

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger('').addHandler(console)

    if args.drawsteps or not args.dontdraw:
        logging.info("Setting up Cairo, size: {}".format(N))
        surface, ctx, size, n = utils.drawing.setup_cairo(N=args.numpoints, scale=SCALE, background=[0,0,0,1], cartesian=True, font_size=FONT_SIZE)
        assert(size == SIZE)
        assert(n == N)
        
        ctx.set_source_rgba(0, 0, 0, 1)
        utils.drawing.drawRect(ctx, 0, 0, size, size)
    
    if args.loaddcel and exists("{}.dcel".format(dcel_filename)):
        logging.info("Loading DCEL")
        theDCEL = utils.dcel.DCEL.loadfile(dcel_filename)
        IPython.embed(simple_prompt=True)
    else:
        logging.info("Initialising DCEL")
        #make the bbox
        bbox = np.array([0,0,SIZE,SIZE])
        theDCEL = utils.dcel.DCEL(bbox=bbox)

        
    #------------------------------
    # def MAIN LOOP
    #------------------------------
    if not args.static:
        logging.info("Generating")
        for x in range(args.timesteps):
            logging.info("Step: {}".format(x))
            should_quit = tick(theDCEL, x)
        
            if args.drawsteps:
                logging.info("Drawing Step: {}".format(x))
                utils.dcel.drawing.drawDCEL(ctx, theDCEL, text=True, faces=True, edges=True, verts=True)
                utils.drawing.write_to_png(surface, saveString, i=x)
                if args.ipython:
                    IPython.embed(simple_prompt=True)
                
            if should_quit:
                break

        #TODO: add in a final verification at the end
            
    #------------------------------
    # def SAVING
    #------------------------------
    save(args, theDCEL)

    #------------------------------
    # def DRAWING
    #------------------------------
    draw(args, theDCEL)
    
    #------------------------------
    # def INSPECTION
    #------------------------------
    if args.ipython:
        IPython.embed(simple_prompt=True)

    
