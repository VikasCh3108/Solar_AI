import graphviz

def create_workflow_diagram_png(output_path):
    dot = graphviz.Digraph(format='png')
    dot.attr(rankdir='TB')  # Top-to-bottom (vertical) layout
    dot.attr('node', shape='box', style='filled', fillcolor='lightyellow')

    dot.node('A', 'User Input')
    dot.node('B', 'Image Acquisition & Preprocessing')
    dot.node('C', 'Rooftop Detection & Segmentation')
    dot.node('D', 'Shading & Obstacle Analysis')
    dot.node('E', 'Solar Potential Assessment')
    dot.node('F', 'System Design & Recommendation')
    dot.node('G', 'Cost & ROI Analysis')
    dot.node('H', 'Report Generation')
    dot.node('I', 'User Feedback & Iteration')

    dot.edge('A', 'B')
    dot.edge('B', 'C')
    dot.edge('C', 'D')
    dot.edge('D', 'E')
    dot.edge('E', 'F')
    dot.edge('F', 'G')
    dot.edge('G', 'H')
    dot.edge('H', 'I')

    dot.render(output_path, cleanup=True)

if __name__ == "__main__":
    create_workflow_diagram_png("workflow_diagram")
    print("Workflow diagram saved as workflow_diagram.png")
