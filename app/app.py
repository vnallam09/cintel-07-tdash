# Penguins Dashboard Application
#
# This Shiny application provides an interactive dashboard to explore Palmer Penguins dataset.
# It allows users to filter and visualize penguin data based on species and body mass,
# displaying various statistics and visualizations.
#
# Dependencies:
#     - seaborn: For data visualization
#     - faicons: For Font Awesome icons
#     - shiny: For creating interactive web applications
#     - palmerpenguins: For the penguin dataset

import seaborn as sns
from faicons import icon_svg
from shiny import reactive
from shiny.express import input, render, ui
import palmerpenguins 

# Load the Palmer Penguins dataset
df = palmerpenguins.load_penguins()

# Custom CSS styles for the dashboard header
ui.tags.head(
    ui.tags.style("""
        /* Header styling with a soft purple background */
        .simple-header {
            background: #8f91b7;
            color: white;
            padding: 1rem;
            margin-bottom: 1rem;
            border-radius: 8px;
            text-align: center;
        }
        
        /* Main title styling */
        .header-title {
            margin: 0;
            font-size: 1.8rem;
            font-weight: 600;
        }
        
        /* Subtitle styling with slightly reduced opacity */
        .header-subtitle {
            margin: 0.5rem 0 0 0;
            font-size: 0.9rem;
            opacity: 0.8;
        }
    """)
)

ui.div(
    ui.h1("🐧 Penguins Dashboard", class_="header-title"),
    ui.p("Explore penguin species data", class_="header-subtitle"),
    class_="simple-header"
)

# Sidebar with interactive filter controls and useful links
with ui.sidebar(title="Filter controls"):
    # Mass filter slider (2000g to 6000g range)
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)
    
    # Species selection checkboxes
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )
    
    # Horizontal line separator
    ui.hr()
    
    # External links section
    ui.h6("Links")
    ui.a(
        "GitHub Source",
        href="https://github.com/vnallam09/cintel-07-tdash",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://vnallam09.github.io/cintel-07-tdash/",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/vnallam09/cintel-07-tdash/issues",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "See also",
        href="https://github.com/vnallam09/pyshiny-penguins-dashboard-express",
        target="_blank",
    )


# Value boxes showing key statistics
with ui.layout_column_wrap(fill=False):
    # First value box: Total count of filtered penguins
    with ui.value_box(showcase=icon_svg("earlybirds")):
        "Number of penguins"

        @render.text
        def count():
            # Calculate and display the total number of penguins in the filtered dataset
            return filtered_df().shape[0]

    # Second value box: Average bill length
    with ui.value_box(showcase=icon_svg("ruler-horizontal")):
        "Average bill length"

        @render.text
        def bill_length():
            # Calculate and display the mean bill length of filtered penguins
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    with ui.value_box(showcase=icon_svg("ruler-vertical")):
        "Average bill depth"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"


# Main dashboard content with visualization and data grid
with ui.layout_columns():
    # Scatter plot card showing relationship between bill length and depth
    with ui.card(full_screen=True):
        ui.card_header("Bill length and depth")

        @render.plot
        def length_depth():
            """
            Create a scatter plot showing the relationship between bill length and depth,
            with points colored by species
            """
            return sns.scatterplot(
                data=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                hue="species",
            )

    # Interactive data grid showing detailed penguin information
    with ui.card(full_screen=True):
        ui.card_header("Penguin Data")

        @render.data_frame
        def summary_statistics():
            """
            Display a filterable data grid with selected columns from the penguin dataset
            """
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)


#ui.include_css(app_dir / "styles.css")


@reactive.calc
def filtered_df():
    """
    Reactive calculation that filters the penguin dataset based on user inputs.
    
    Returns:
        pandas.DataFrame: Filtered dataset containing only the selected species
        and penguins with body mass less than the specified threshold.
    """
    # Filter by selected species
    filt_df = df[df["species"].isin(input.species())]
    
    # Filter by maximum body mass
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    
    return filt_df
