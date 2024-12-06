from sskit import load_camera, imread, imwrite, project_on_ground, undistort_image, look_at
from pathlib import Path

def test_basic():
    d = Path("example")
    camera_matrix, dist_poly, undist_poly = load_camera(d)
    img = imread(d / "rgb.jpg")
    imwrite(img, "t.png")
    _, h, w = img.shape

    tst = project_on_ground(camera_matrix, dist_poly, img[None], height=50, center=[0,-25])
    imwrite(tst, "t.png")

    tst = undistort_image(dist_poly, img[None], 0.5)
    imwrite(tst, "t.png")

    tst = look_at(camera_matrix, dist_poly, img[None], [0,0,0])
    imwrite(tst, "t.png")
