import numpy as np
from intercept import Intercept
from math import pi, atan2, acos


class Shape(object):
    def __init__(self, position, material):
        self.position = position
        self.material = material
        self.type = "None"

    def ray_intersect(self, orig, dir):
        return None
    
class Sphere(Shape):
    def __init__(self, position, radius, material):
        super().__init__(position, material)
        self.radius = radius
        self.type = "Sphere"

    def ray_intersect(self, orig, dir):
        L = np.subtract(self.position, orig)
        tca = np.dot(L, dir)
        d = (np.linalg.norm(L) **2 - tca **2) **0.5

        if d>self.radius:
            return None
        
        thc = (self.radius **2 - d**2) **0.5

        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return None        
        
        P = np.add(orig, np.multiply(dir, t0))

        normal = np.subtract(P, self.position)
        normal /= np.linalg.norm(normal)

        u = -atan2(normal[2], normal[0]) / (2 * pi) + 0.5
        v = acos(-normal[1]) / pi


        return Intercept(point=P,
                         normal=normal, 
                         distance=t0,
                         texCoords= [u, v], 
                         rayDirection = dir, 
                         obj=self)

class Plane(Shape):
    def __init__(self, position, normal, material):
        super().__init__(position, material)
        self.normal = normal / np.linalg.norm(normal)
        self.type = "Plane"
    
    def ray_intersect(self, orig, dir):
        denom = np.dot(dir, self.normal)
        if abs(denom) < 1e-6:  
            return None
        
        t = np.dot(np.subtract(self.position, orig), self.normal) / denom
        
        if t < 1e-6:
            return None

        P = np.add(orig, np.multiply(dir, t))

        return Intercept(point=P,
                        normal=self.normal, 
                        distance=t,
                        texCoords=None,
                        rayDirection=dir, 
                        obj=self)

class Disk(Plane):
    def __init__(self, position, normal, radius, material):
        super().__init__(position, normal, material)
        self.radius = radius
        self.type = "Disk"
    
    def ray_intersect(self, orig, dir):
        planeIntercept = super().ray_intersect(orig, dir)
        
        if planeIntercept is None:
            return None
        
        vectorToCenter = np.subtract(planeIntercept.point, self.position)
        distanceSquared = np.dot(vectorToCenter, vectorToCenter)
        
        if distanceSquared <= self.radius **2:
            return planeIntercept
        else:
            return None

class AABB(Shape):
    def __init__(self, position, sizes, material):
        super().__init__(position, material)
        self.sizes = sizes
        self.type = "AABB"

        self.planes = []

        rightPlane = Plane([position[0] + sizes[0]/2, position[1], position[2]], [1, 0, 0], material)
        leftPlane = Plane([position[0] -sizes[0]/2, position[1], position[2]], [-1, 0, 0], material)

        upPlane = Plane([position[0], position[1] + sizes[1]/2, position[2]], [0, 1, 0], material)
        downPlane = Plane([position[0], position[1] - sizes[1]/2, position[2]], [0, -1, 0], material)

        frontPlane = Plane([position[0], position[1], position[2] + sizes[2]/2], [0,0,1], material)
        backPlane = Plane([position[0], position[1], position[2] - sizes[2]/2], [0,0,-1], material)

        self.planes.append(rightPlane)
        self.planes.append(leftPlane)
        self.planes.append(upPlane)
        self.planes.append(downPlane)
        self.planes.append(frontPlane)
        self.planes.append(backPlane)

        self.boundsMin = [0,0,0]
        self.boundsMax = [0,0,0]

        epsilon = 0.001

        for i in range(3):
            self.boundsMin[i] = position[i] - (epsilon + sizes[i]/2)
            self.boundsMax[i] = position[i] + (epsilon + sizes[i]/2)

    def ray_intersect(self, orig, dir):
        orig = np.array(orig)
        dir = np.array(dir)
        boundsMin = np.array(self.boundsMin)
        boundsMax = np.array(self.boundsMax)
        
        # Eje X
        if abs(dir[0]) < 1e-10:
            if orig[0] < boundsMin[0] or orig[0] > boundsMax[0]:
                return None
            t0x = float('-inf')
            t1x = float('inf')
        else:
            invdx = 1.0 / dir[0]
            t0x = (boundsMin[0] - orig[0]) * invdx
            t1x = (boundsMax[0] - orig[0]) * invdx
            if t0x > t1x:
                t0x, t1x = t1x, t0x
        
        # Eje Y
        if abs(dir[1]) < 1e-10:
            if orig[1] < boundsMin[1] or orig[1] > boundsMax[1]:
                return None
            t0y = float('-inf')
            t1y = float('inf')
        else:
            invdy = 1.0 / dir[1]
            t0y = (boundsMin[1] - orig[1]) * invdy
            t1y = (boundsMax[1] - orig[1]) * invdy
            if t0y > t1y:
                t0y, t1y = t1y, t0y
        
        tmin = max(t0x, t0y)
        tmax = min(t1x, t1y)
        
        if tmin > tmax:
            return None
        
        # Eje Z
        if abs(dir[2]) < 1e-10:
            if orig[2] < boundsMin[2] or orig[2] > boundsMax[2]:
                return None
            t0z = float('-inf')
            t1z = float('inf')
        else:
            invdz = 1.0 / dir[2]
            t0z = (boundsMin[2] - orig[2]) * invdz
            t1z = (boundsMax[2] - orig[2]) * invdz
            if t0z > t1z:
                t0z, t1z = t1z, t0z
        
        tmin = max(tmin, t0z)
        tmax = min(tmax, t1z)
        
        if tmin > tmax:
            return None
        
        t = tmin
        if t < 1e-6:
            t = tmax
            if t < 1e-6:
                return None
        
        P = orig + dir * t
        
        normal = np.array([0.0, 0.0, 0.0])
        center = np.array(self.position)
        epsilon = 1e-5
        
        relativePos = P - center
        halfSizes = np.array(self.sizes) / 2
        
        if abs(abs(relativePos[0]) - halfSizes[0]) < epsilon:
            normal[0] = 1.0 if relativePos[0] > 0 else -1.0
        elif abs(abs(relativePos[1]) - halfSizes[1]) < epsilon:
            normal[1] = 1.0 if relativePos[1] > 0 else -1.0
        elif abs(abs(relativePos[2]) - halfSizes[2]) < epsilon:
            normal[2] = 1.0 if relativePos[2] > 0 else -1.0
        else:
            maxAxis = np.argmax(np.abs(relativePos / halfSizes))
            normal[maxAxis] = 1.0 if relativePos[maxAxis] > 0 else -1.0
        
        return Intercept(point=P,
                        normal=normal, 
                        distance=t,
                        texCoords=None,
                        rayDirection=dir, 
                        obj=self)

class Triangle(Plane):
    def __init__(self, A, B, C, material):

        super().__init__(position=None, material=material)
        self.A = np.array(A)
        self.B = np.array(B) 
        self.C = np.array(C)
        self.type = "Triangle"
        
        BA = np.subtract(self.B, self.A)
        BC = np.subtract(self.B, self.C)
        self.normal = np.cross(BA, BC)
        self.normal = self.normal / np.linalg.norm(self.normal)

    def ray_intersect(self, orig, dir):
        
        edge1 = np.subtract(self.B, self.A)
        edge2 = np.subtract(self.C, self.A)
        
        h = np.cross(dir, edge2)
        a = np.dot(edge1, h)
        
        if abs(a) < 1e-6:
            return None
        
        f = 1.0 / a
        s = np.subtract(orig, self.A)
        u = f * np.dot(s, h)
        
        if u < 0.0 or u > 1.0:
            return None
        
        q = np.cross(s, edge1)
        v = f * np.dot(dir, q)
        
        if v < 0.0 or u + v > 1.0:
            return None
        
        t = f * np.dot(edge2, q)
        
        if t < 1e-6:
            return None
        
        P = np.add(orig, np.multiply(dir, t))
        
        return Intercept(point=P,
                        normal=self.normal,
                        distance=t,
                        texCoords=None,
                        rayDirection=dir,
                        obj=self)
    

class Cilindro(Shape):
    def __init__(self, position, height, radius, material):
        super().__init__(position, material)
        self.radius = radius
        self.height = height
        self.type = "Cilindro"
        
        bottom_pos = [position[0], position[1] - height/2, position[2]]
        top_pos = [position[0], position[1] + height/2, position[2]]
        
        self.bottom_disk = Disk(bottom_pos, [0, -1, 0], radius, material)
        self.top_disk = Disk(top_pos, [0, 1, 0], radius, material)

    def ray_intersect(self, orig, dir):
        orig = np.array(orig)
        dir = np.array(dir)
        pos = np.array(self.position)

        minY = pos[1] - self.height / 2
        maxY = pos[1] + self.height / 2

        dxz = np.array([dir[0], 0, dir[2]])
        oxz = np.array([orig[0], 0, orig[2]])
        cxz = np.array([pos[0], 0, pos[2]])

        L = oxz - cxz
        a = np.dot(dxz, dxz)
        
        intercept = None
        
        if a > 1e-10:
            b = 2 * np.dot(dxz, L)
            c = np.dot(L, L) - self.radius ** 2

            discriminant = b * b - 4 * a * c
            
            if discriminant >= 0:
                sqrt_disc = np.sqrt(discriminant)
                t0 = (-b - sqrt_disc) / (2 * a)
                t1 = (-b + sqrt_disc) / (2 * a)

                for t in [t0, t1]:
                    if t > 1e-6:
                        P = orig + dir * t
                        if minY <= P[1] <= maxY:
                            if intercept is None or t < intercept.distance:
                                normal = P - pos
                                normal[1] = 0
                                normal = normal / np.linalg.norm(normal)
                                intercept = Intercept(point=P,
                                                             normal=normal,
                                                             distance=t,
                                                             texCoords=None,
                                                             rayDirection=dir,
                                                             obj=self)
                                

        bottom_intercept = self.bottom_disk.ray_intersect(orig, dir)
        if bottom_intercept is not None:
            if intercept is None or bottom_intercept.distance < intercept.distance:
                intercept = bottom_intercept
                intercept.obj = self

        top_intercept = self.top_disk.ray_intersect(orig, dir)
        if top_intercept is not None:
            if intercept is None or top_intercept.distance < intercept.distance:
                intercept = top_intercept
                intercept.obj = self

        return intercept
    
class Elipsoide(Shape):
    def __init__(self, position, radius, material):
        super().__init__(position, material)
        self.radius = np.array(radius)
        self.type = "Elipsoide"

    def ray_intersect(self, orig, dir):
        orig = np.array(orig)
        dir = np.array(dir)
        pos = np.array(self.position)

        O = orig - pos  
        D = dir        
        a, b, c = self.radius

        A = (D[0] * D[0]) / (a * a) + (D[1] * D[1]) / (b * b) + (D[2] * D[2]) / (c * c)
        B = 2.0 * ( (O[0] * D[0]) / (a * a) + (O[1] * D[1]) / (b * b) + (O[2] * D[2]) / (c * c) )
        C = (O[0] * O[0]) / (a * a) + (O[1] * O[1]) / (b * b) + (O[2] * O[2]) / (c * c) - 1.0

        eps = 1e-12
        if abs(A) < eps:
            return None

        discr = B * B - 4.0 * A * C
        if discr < 0:
            return None

        sqrt_disc = np.sqrt(discr)
        t0 = (-B - sqrt_disc) / (2.0 * A)
        t1 = (-B + sqrt_disc) / (2.0 * A)

        t = None
        if t0 > 1e-6 and t1 > 1e-6:
            t = min(t0, t1)
        elif t0 > 1e-6:
            t = t0
        elif t1 > 1e-6:
            t = t1
        else:
            return None

        P = orig + dir * t
        Pr = P - pos
        x, y, z = Pr

        normal = np.array([2.0 * x / (a * a),
                           2.0 * y / (b * b),
                           2.0 * z / (c * c)])
        norm_len = np.linalg.norm(normal)
        if norm_len == 0:
            return None
        normal /= norm_len


        return Intercept(point=P,
                         normal=normal,
                         distance=t,
                         texCoords=None,
                         rayDirection=dir,
                         obj=self)
    


class Toroide(Shape):
    def __init__(self, position, R, r, material):
       
        super().__init__(position, material)
        self.R = R
        self.r = r
        self.type = "Toroide"

    def ray_intersect(self, orig, dir):
        orig = np.array(orig)
        dir = np.array(dir)
        pos = np.array(self.position)

        O = orig - pos
        D = dir

        Dx, Dy, Dz = D
        Ox, Oy, Oz = O

        G = np.dot(D, D)
        H = 2 * np.dot(O, D)
        I = np.dot(O, O) + self.R**2 - self.r**2

        A = G**2
        B = 2 * G * H
        C = H**2 + 2 * G * I - 4 * self.R**2 * (Dx**2 + Dz**2)
        Dcoef = 2 * H * I - 8 * self.R**2 * (Ox * Dx + Oz * Dz)
        E = I**2 - 4 * self.R**2 * (Ox**2 + Oz**2)

        coeffs = [A, B, C, Dcoef, E]
        roots = np.roots(coeffs)
        roots = np.real(roots[np.isreal(roots)])  
        roots = roots[roots > 1e-6]  

        if len(roots) == 0:
            return None

        t = np.min(roots)
        P = orig + dir * t 

        Pr = P - pos
        x, y, z = Pr
        sum_sq = x**2 + y**2 + z**2
        factor = 4.0 * (sum_sq - self.R**2 - self.r**2)
        normal = np.array([
            factor * x - 8.0 * self.R**2 * x / (x**2 + z**2) * (x**2 + z**2 > 1e-8),
            factor * y,
            factor * z - 8.0 * self.R**2 * z / (x**2 + z**2) * (x**2 + z**2 > 1e-8)
        ])
        norm_len = np.linalg.norm(normal)
        if norm_len == 0:
            return None
        normal /= norm_len

        theta = np.arctan2(z, x) 
        local_r = np.sqrt(x**2 + z**2) - self.R
        phi = np.arctan2(y, local_r) 

        u = (theta + np.pi) / (2 * np.pi)
        v = (phi + np.pi) / (2 * np.pi)

        return Intercept(point=P,
                         normal=normal,
                         distance=t,
                         texCoords=[u, v],
                         rayDirection=dir,
                         obj=self)
    
class Cone(Shape):
    def __init__(self, position, height, radius, material):
        super().__init__(position, material)
        self.height = height
        self.radius = radius
        self.type = "Cone"

        self.vertex = np.array([position[0], position[1] + height / 2, position[2]])
        self.base_center = np.array([position[0], position[1] - height / 2, position[2]])
        self.angle = np.arctan(radius / height)  

        self.base_disk = Disk(self.base_center, [0, -1, 0], radius, material)

    def ray_intersect(self, orig, dir):
        orig = np.array(orig)
        dir = np.array(dir)

        co = orig - self.vertex
        cos2 = np.cos(self.angle) ** 2
        sin2 = np.sin(self.angle) ** 2

        dx, dy, dz = dir
        ox, oy, oz = co

        A = dx**2 + dz**2 - (dy**2 * (self.radius**2 / self.height**2))
        B = 2 * (ox * dx + oz * dz - (oy * dy * (self.radius**2 / self.height**2)))
        C = ox**2 + oz**2 - (oy**2 * (self.radius**2 / self.height**2))

        discr = B**2 - 4 * A * C
        if discr < 0:
            return None

        sqrt_disc = np.sqrt(discr)
        t0 = (-B - sqrt_disc) / (2 * A)
        t1 = (-B + sqrt_disc) / (2 * A)

        t = None
        for ti in [t0, t1]:
            if ti > 1e-6:
                P = orig + dir * ti
                y = P[1]
                if self.base_center[1] <= y <= self.vertex[1]: 
                    t = ti
                    break

        if t is None:
            return self.base_disk.ray_intersect(orig, dir)

        P = orig + dir * t
        v = P - self.vertex
        v_proj = np.array([v[0], 0, v[2]])
        n = np.array([v[0], np.linalg.norm(v_proj) * (self.radius / self.height), v[2]])
        n = n / np.linalg.norm(n)

        return Intercept(point=P,
                        normal=n,
                        distance=t,
                        texCoords=None,
                        rayDirection=dir,
                        obj=self)

