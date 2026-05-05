import pandas as pd
import pygmt

# =========================
# USER SETTINGS
# =========================
csv_file = r"D:\Map\Sprat_gracilis_sites.csv"
output_file = r"D:\Map\Sprat_gracilis_Philippines_Map_gradient_style_oleron.png"

# Main map extent for whole Philippines: [west, east, south, north]
region_main = [116, 127, 4, 21]

# Tighter inset extent if needed later
region_inset = [104, 130, 1, 24]

# Site column names
lon_col = "Longitude"
lat_col = "Latitude"
site_col = "Site"

# -------------------------
# LABEL COLORS
# -------------------------
site_label_color = "black"
geo_label_color = "black"
sea_label_color = "black"

# =========================
# READ CSV
# =========================
df = pd.read_csv(csv_file)

for col in [lon_col, lat_col]:
    if col not in df.columns:
        raise ValueError(
            f"Column '{col}' not found in CSV. Found columns: {list(df.columns)}"
        )

if site_col not in df.columns:
    df[site_col] = [f"Site {i+1}" for i in range(len(df))]

# =========================
# ASSIGN THREE MARKER TYPES
# =========================
marker_styles = ["c0.5c", "s0.5c", "t0.5c"]
marker_colors = ["red", "dodgerblue", "gold"]

df = df.copy()
df["marker_style"] = [marker_styles[i % 3] for i in range(len(df))]
df["marker_color"] = [marker_colors[i % 3] for i in range(len(df))]

# =========================
# LOAD BATHYMETRY
# =========================
grid = pygmt.datasets.load_earth_relief(
    resolution="30s",
    region=region_main,
)

# =========================
# CONTINUOUS DEPTH CPT
# Method 3: built-in colormap
# =========================
cpt_file = r"D:\Map\phil_depth_gradient.cpt"

pygmt.makecpt(
    cmap="oleron", #alternatives# try "batlowW", "deep", "oleron", "geo"
    series=[-10000, -10],
    continuous=True,
    reverse=False,
    output=cpt_file,
)

# =========================
# SITE LEGEND FILE
# =========================
site_legend_file = r"D:\Map\phil_sites_legend.txt"
with open(site_legend_file, "w", encoding="utf-8") as f:
    f.write("H 12p,Helvetica-Bold,black Sites\n")
    f.write("D 0.15c 1p\n")
    f.write("S 0.30c c 0.32c red 0.7p,black 0.7c Jolo\n")
    f.write("S 0.30c s 0.32c dodgerblue 0.7p,black 0.7c Palapag\n")
    f.write("S 0.30c t 0.36c gold 0.7p,black 0.7c Matalvi\n")

# =========================
# GLOBAL STYLE
# =========================
with pygmt.config(
    FONT_ANNOT_PRIMARY="12p,Helvetica,black",
    FONT_LABEL="12p,Helvetica-Bold,black",
    FONT_TITLE="14p,Helvetica-Bold,black",
    MAP_FRAME_PEN="1.5p,black",
    MAP_TICK_PEN_PRIMARY="1.5p,black",
    MAP_FRAME_TYPE="plain",
):
    fig = pygmt.Figure()

    # -------------------------
    # MAIN MAP
    # -------------------------
    fig.basemap(
        region=region_main,
        projection="M16c",
        frame=['WSe+t', "xa2", "ya2"],
    )

    fig.grdimage(
        grid=grid,
        cmap=cpt_file,
        shading=False,
    )

    fig.coast(
        land="lightgray",
        shorelines="0.6p,black",
        borders="1/0.4p,gray40",
    )

    # -------------------------
    # SITES WITH 3 MARKERS
    # -------------------------
    for style, color in zip(marker_styles, marker_colors):
        subset = df[df["marker_style"] == style]
        fig.plot(
            x=subset[lon_col],
            y=subset[lat_col],
            style=style,
            fill=color,
            pen="0.4p,black",
        )

    for _, row in df.iterrows():
        fig.text(
            x=row[lon_col] + 0.10,
            y=row[lat_col] + 0.10,
            text=str(row[site_col]),
            font=f"12p,Helvetica-Bold,{site_label_color}",
            justify="LM",
        )

    # -------------------------
    # COUNTRY / ISLAND LABELS
    # -------------------------
    geo_label_data = [
        (121.0, 17.0, "LUZON"),
        (124.6, 10.8, "VISAYAS"),
        (125.0, 8.0, "MINDANAO"),
        (118.6, 10.3, "PALAWAN"),
    ]

    for x, y, txt in geo_label_data:
        fig.text(
            x=x,
            y=y,
            text=txt,
            font=f"13p,Helvetica-Bold,{geo_label_color}",
            justify="CM",
        )

    # -------------------------
    # SEA LABELS
    # -------------------------
    sea_label_data = [
        (118.3, 14.0, "WEST PHILIPPINE SEA"),
        (124.9, 15.0, "PHILIPPINE SEA"),
        (120.0, 8.0, "SULU SEA"),
        (123.3, 5.0, "CELEBES SEA"),
        (124.0, 9.0, "BOHOL SEA"),
    ]

    for x, y, txt in sea_label_data:
        fig.text(
            x=x,
            y=y,
            text=txt,
            font=f"13p,Helvetica-Bold,{sea_label_color}",
            justify="CM",
        )

    # -------------------------
    # SCALE BAR
    # -------------------------
    fig.basemap(
        map_scale="jBL+w200k+o0.6c/1.75c+f+lkm",
    )

    # -------------------------
    # NORTH ARROW
    # -------------------------
    fig.basemap(
        rose="jTR+w1.2c+o0.5c/0.5c+f2+p1p,black"
    )

    # -------------------------
    # VERTICAL DEPTH COLORBAR
    # -------------------------
    fig.colorbar(
        cmap=cpt_file,
        position="JMR+jML+o0.7c/1.5c+w6c/0.5c+v",
        frame=["xaf2000+lDepth (m)"],
    )

    # -------------------------
    # SITE LEGEND
    # -------------------------
    fig.legend(
        spec=site_legend_file,
        position="JMR+jML+o0.3c/-3.5c",
    )

    # -------------------------
    # SAVE
    # -------------------------
    fig.savefig(output_file, dpi=600)

print(f"Map saved to: {output_file}")