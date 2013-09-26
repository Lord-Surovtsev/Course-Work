#!/usr/bin/python
"""
the script demostrates iterative construction of
delaunay triangulation and voronoi tesselation

Original Author (C version): ?
Converted to Python by: Roman Stanchak
"""
import cv2.cv as cv
import random


def draw_subdiv_edge( img, edge, color ):
    org_pt = cv.Subdiv2DEdgeOrg(edge);
    dst_pt = cv.Subdiv2DEdgeDst(edge);

    if org_pt and dst_pt :

        org = org_pt.pt;
        dst = dst_pt.pt;

        iorg = ( cv.Round( org[0] ), cv.Round( org[1] ));
        idst = ( cv.Round( dst[0] ), cv.Round( dst[1] ));

        cv.Line( img, iorg, idst, color, 1, cv.CV_AA, 0 );


def draw_subdiv( img, subdiv, delaunay_color, voronoi_color ):

    for edge in subdiv.edges:
        edge_rot = cv.Subdiv2DRotateEdge( edge, 1 )

        draw_subdiv_edge( img, edge_rot, voronoi_color );
        draw_subdiv_edge( img, edge, delaunay_color );

def Tesselation(P, (width, height)):
    win = "source";
    rect = ( 0, 0, height, width);

    active_facet_color = cv.RGB( 255, 0, 0 );
    delaunay_color  = cv.RGB( 0,0,0);
    voronoi_color = cv.RGB(0, 180, 0);
    bkgnd_color = cv.RGB(255,255,255);

    img = cv.CreateImage( (rect[2],rect[3]), 8, 3 );
    cv.Set( img, bkgnd_color );

    cv.NamedWindow( win, 1 );

    storage = cv.CreateMemStorage(0);
    subdiv = cv.CreateSubdivDelaunay2D( rect, storage );

    print "Delaunay triangulation will be build now interactively."
    print "To stop the process, press any key\n"

    for i in range(len(P)):
#        fp = ( random.random()*(rect[2]-10)+5, random.random()*(rect[3]-10)+5 )
#        x = input()
#        y = input()
#        fp = (x, y)
#        print "point ", P[i][0], " ", P[i][1]
#        print "randomP ", ( random.random()*(rect[2]-10)+5, random.random()*(rect[3]-10)+5 )
        fp = (P[i][0], P[i][1])
#        locate_point( subdiv, fp, img, active_facet_color );
        cv.ShowImage( win, img );


        cv.SubdivDelaunay2DInsert( subdiv, fp );
#        cv.CalcSubdivVoronoi2D( subdiv );
        cv.Set( img, bkgnd_color );
        draw_subdiv( img, subdiv, delaunay_color, voronoi_color );
        cv.ShowImage( win, img );

    cv.Set( img, bkgnd_color );

    cv.WaitKey(0);

    cv.DestroyWindow( win );

