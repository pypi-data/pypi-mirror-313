import os.path
from pathlib import Path

from digitalarztools.pipelines.gmap.poi import GMapPipeline
from digitalarztools.io.vector.gpd_vector import GPDVector

if __name__ == "__main__":
    current_dir = os.path.dirname(__file__)
    kml_path = os.path.join(current_dir,'media/Neighbourhood_AlAhyah.kml')
    kml_name = Path(kml_path).stem
    gdv = GPDVector.from_kml(kml_path)
    gmap = GMapPipeline()
    gmap.download_poi(gdv, search_radius=1000, boundary_name=kml_name)