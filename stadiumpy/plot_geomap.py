import pygmt
import numpy as np

minlon, maxlon = 70, 100
minlat, maxlat = 0, 35
res='i'


#define etopo data file
topo_data = '@earth_relief_01m' #30 arc second global relief (SRTM15+V2.1 @ 1.0 km)

def plot_map(minlon,maxlon,minlat, maxlat,topo_data,outputfile,res='i', width="8c", frame="f"):
    print(f"Plotting map for {minlon},{maxlon},{minlat},{maxlat}")
    fig = pygmt.Figure()

    # make color pallets
    pygmt.makecpt(
        cmap='geo',
        series='-8000/11000/1000',
        continuous=True
    )

    #plot high res topography
    fig.grdimage(
        grid=topo_data,
        region=[minlon, maxlon, minlat, maxlat], 
        projection='M'+width,
        shading=True,
        frame=frame
        )

    fig.coast( region=[minlon, maxlon, minlat, maxlat],
        resolution=res,
        shorelines=["1/0.2p,black", "2/0.05p,gray"],
        borders=1, #political boundary
    )
    # fig.colorbar(
    #     position="JCR+v",
    #     frame=["x2000","y+lm"]
    # )

    fig.savefig(outputfile, crop=True, dpi=300)
    # fig.savefig(".stadiumpyCache/region-plot.png", crop=True, dpi=300)
    print("Map ready")

if __name__ == "__main__":
    minlon, maxlon = 70, 100
    minlat, maxlat = 0, 35
    res='i'


    #define etopo data file
    topo_data = '@earth_relief_01m' #30 arc second global relief (SRTM15+V2.1 @ 1.0 km)
    # plot_map(minlon,maxlon,minlat, maxlat,topo_data,res='i')