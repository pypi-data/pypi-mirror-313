# python setup.py sdist bdist_wheel
# twine upload dist/*
import os
import shutil
from setuptools import setup, find_packages

requirements = [
    'tqdm~=4.66.2',
    'shapely~=2.0.1',
    'protobuf~=5.26.1',
    'fiona~=1.10.0',
    'pyproj~=3.6.1',
    'pyclipper~=1.3.0',
    'h3~=4.1.1',
    'pandas~=2.2.3'
],

def clean_build():
    build_dir = 'build'
    dist_dir = 'dist'
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)

clean_build()

setup(
    name='vgrid',
    version='1.1.10',
    author = 'Thang Quach',
    author_email= 'quachdongthang@gmail.com',
    url='https://github.com/thangqd/vgrid',
    description='Vgrid - Global Geocoding Systems',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    requires_python=">=3.0",
    packages=find_packages(),
    include_package_data=True,  # Include package data specified in MANIFEST.in
    entry_points={
        'console_scripts': [            
            'vcode2geojson = vgrid.geocode.vcode:vcode2geojson_cli',  
            'vencode = vgrid.geocode.vcode:vencode_cli',  
            'vdecode = vgrid.geocode.vcode:vdecode_cli',  
            
            'olc2geojson = vgrid.geocode.geocode2geojson:olc2geojson_cli',  
            'maidenhead2geojson = vgrid.geocode.geocode2geojson:maidenhead2geojson_cli',  
            'gars2geojson = vgrid.geocode.geocode2geojson:gars2geojson_cli',  
            'geohash2geojson = vgrid.geocode.geocode2geojson:geohash2geojson_cli',  
            'mgrs2geojson = vgrid.geocode.geocode2geojson:mgrs2geojson_cli',  
            'georef2geojson = vgrid.geocode.geocode2geojson:georef2geojson_cli',  
            'h32geojson = vgrid.geocode.geocode2geojson:h32geojson_cli',  
            's22geojson = vgrid.geocode.geocode2geojson:s22geojson_cli',  


            'vgrid = vgrid.grid.vgrid:main',   
            'gzd = vgrid.grid.gzd:main',  
            'mgrsgrid = vgrid.grid.mgrsgrid:main',
            'geohashgrid = vgrid.grid.geohashgrid:main',           
            'maidenheadgrid = vgrid.grid.maidenheadgrid:main',           
            # 'olcgrid = vgrid.grid.olcgrid:main',
            'h3grid = vgrid.grid.h3grid:main',
            's2grid = vgrid.grid.s2grid:main',

            'rhealpixstats = vgrid.stats.rhealpixstats:main'   ,
            'h3stats = vgrid.stats.h3stats:main',
            's2stats = vgrid.stats.s2stats:main',

            # 'olcstats = vgrid.stats.olcstats:main',
            'geohashstats = vgrid.stats.geohashstats:main',
            'maidenheadstats = vgrid.stats.maidenheadstats:main',
            'garsstats = vgrid.stats.garsstats:main',
            'georefstats = vgrid.stats.georefstats:main',
            'mgrsstats = vgrid.stats.mgrsstats:main',

        ],
    },    

    install_requires=requirements,    
    classifiers=[
        'Programming Language :: Python :: 3',
        'Environment :: Console',
        'Topic :: Scientific/Engineering :: GIS',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
