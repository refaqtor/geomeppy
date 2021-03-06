# Copyright (c) 2016 Jamie Bull
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""pytest for transformations.py"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from transforms3d._gohlketransforms import translation_matrix

from geomeppy.polygons import Polygon3D
from geomeppy.transformations import Transformation
from geomeppy.vectors import Vector3D
import numpy as np
from geomeppy.utilities import almostequal


class TestTransormations():
    
    def test_translation_transformations(self):
        tol = 12 # places
        trans = Vector3D(1,1,1)
        point1 = Vector3D(1,0,0)
        t = Transformation()
        
        # identity transformation
        temp = t * point1
        assert almostequal(1.0, temp.x, tol)
        assert almostequal(0.0, temp.y, tol)
        assert almostequal(0.0, temp.z, tol)
        
        # move by 1, 1, 1
        t = Transformation(translation_matrix(trans))
        temp = t * point1
        assert almostequal(2.0, temp.x, tol)
        assert almostequal(1.0, temp.y, tol)
        assert almostequal(1.0, temp.z, tol)
        
        # move by -1, -1, -1
        temp = t.inverse() * point1
        assert almostequal(0.0, temp.x, tol)
        assert almostequal(-1.0, temp.y, tol)
        assert almostequal(-1.0, temp.z, tol)
        
        # identity transformation
        temp = t.inverse() * t * point1
        assert almostequal(1.0, temp.x, tol)
        assert almostequal(0.0, temp.y, tol)
        assert almostequal(0.0, temp.z, tol)
        
        # identity transformation
        temp = t * t.inverse() * point1
        assert almostequal(1.0, temp.x, tol)
        assert almostequal(0.0, temp.y, tol)
        assert almostequal(0.0, temp.z, tol)
    
    def test_align_z_prime_transformations(self):
        x_axis = Vector3D(1,0,0)
        y_axis = Vector3D(0,1,0)
        z_axis = Vector3D(0,0,1)
        t = Transformation()
        
        outward_normal = Vector3D(0, -1, 0)
        t = t.align_z_prime(outward_normal)
        assert x_axis == t * x_axis
        assert z_axis == t * y_axis
        result = t * z_axis
        assert outward_normal == result
        
        outward_normal = Vector3D(1, 0, 0)
        t = t.align_z_prime(outward_normal)
        assert y_axis == t * x_axis
        assert z_axis == t * y_axis
        assert outward_normal == t * z_axis
        
        outward_normal = Vector3D(0, 1, 0)
        t = t.align_z_prime(outward_normal)
        assert -x_axis == t * x_axis
        assert z_axis == t * y_axis
        assert outward_normal == t * z_axis
        
        outward_normal = Vector3D(-1, 0, 0)
        t = t.align_z_prime(outward_normal)
        assert -y_axis == t * x_axis
        assert z_axis == t * y_axis
        assert outward_normal == t * z_axis
        
        outward_normal = Vector3D(0, 0, 1)
        t = t.align_z_prime(outward_normal)
        assert -x_axis == t * x_axis
        assert -y_axis == t * y_axis
        assert outward_normal == t * z_axis
        
        outward_normal = Vector3D(0, 0, -1)
        t = t.align_z_prime(outward_normal)
        assert -x_axis == t * x_axis
        assert y_axis == t * y_axis
        assert outward_normal == t * z_axis
    
    def test_align_face_transformations(self):
        tol = 12  # places
        
        vertices = Polygon3D([(1, 0, 1), (1, 0, 0), (2, 0, 0), (2, 0, 1)])
        t = Transformation()
        
        # rotate 0 degrees about z
        testVertices = t.rotation(Vector3D(0,0,1), 0) * vertices
        t = Transformation().align_face(testVertices)
        tempVertices = t.inverse() * testVertices
        expectedVertices = Polygon3D([(0,1,0),(0,0,0),(1,0,0),(1,1,0)])
        assert almostequal(tempVertices, expectedVertices, tol)
    
        # rotate 30 degrees about z
        testVertices = t.rotation(Vector3D(0,0,1), np.deg2rad(30)) * vertices
        t = Transformation().align_face(testVertices)
        tempVertices = t.inverse() * testVertices
        expectedVertices = Polygon3D([(0,1,0),(0,0,0),(1,0,0),(1,1,0)])
        assert almostequal(tempVertices, expectedVertices, tol)
    
        # rotate -30 degrees about z
        testVertices = t.rotation(Vector3D(0,0,1), -np.deg2rad(30)) * vertices
        t = Transformation().align_face(testVertices)
        tempVertices = t.inverse() * testVertices
        expectedVertices = Polygon3D([(0,1,0),(0,0,0),(1,0,0),(1,1,0)])
        assert almostequal(tempVertices, expectedVertices, tol)
    
        # rotate -30 degrees about x
        testVertices = t.rotation(Vector3D(1,0,0), -np.deg2rad(30)) * vertices
        t = Transformation().align_face(testVertices)
        tempVertices = t.inverse() * testVertices    
        expectedVertices = Polygon3D([(0,1,0),(0,0,0),(1,0,0),(1,1,0)])
        assert almostequal(tempVertices, expectedVertices, tol)
    
        # rotate -90 degrees about x
        testVertices = t.rotation(Vector3D(1,0,0), -np.deg2rad(90)) * vertices
        t = Transformation().align_face(testVertices)
        tempVertices = t.inverse() * testVertices
        expectedVertices = Polygon3D([(1,0,0),(1,1,0),(0,1,0),(0,0,0)])
        assert almostequal(tempVertices, expectedVertices, tol)
    
        # rotate 30 degrees about x
        testVertices = t.rotation(Vector3D(1,0,0), np.deg2rad(30)) * vertices
        t = Transformation().align_face(testVertices)
        tempVertices = t.inverse() * testVertices    
        expectedVertices = Polygon3D([(0,1,0),(0,0,0),(1,0,0),(1,1,0)])
        assert almostequal(tempVertices, expectedVertices, tol)
    
        # rotate 90 degrees about x
        testVertices = t.rotation(Vector3D(1,0,0), np.deg2rad(90)) * vertices
        t = Transformation().align_face(testVertices)
        tempVertices = t.inverse() * testVertices    
        expectedVertices = Polygon3D([(1,0,0),(1,1,0),(0,1,0),(0,0,0)])
        assert almostequal(tempVertices, expectedVertices, tol)
    
    
    def test_align_face_transformations_trapezoid_floor(self):
        tol = 12  # places
        
        testVertices = Polygon3D([(27.69,0,0),(0,0,0),
                                  (5,5,0),(22.69,5,0)])
        t = Transformation().align_face(testVertices)
        tempVertices = t.inverse() * testVertices
        expectedVertices = Polygon3D([(0,0,0),(27.69,0,0),(22.69,5,0),(5,5,0)])
        assert almostequal(tempVertices, expectedVertices, tol)
