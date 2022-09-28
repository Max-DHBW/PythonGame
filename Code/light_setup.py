from panda3d.core import PointLight, AmbientLight

def setup_point_light(render, pos):
    plight = PointLight("point_light")
    plight.setColor((1, 1, 1, 1))
    plnp = render.attachNewNode(plight)
    plnp.setPos(pos[0], pos[1], pos[2])
    render.setLight(plnp)
