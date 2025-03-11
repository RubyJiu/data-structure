from graphviz import Digraph

def create_basketball_analysis_flowchart():
    # Create a new directed graph
    dot = Digraph(comment='Basketball Data Analysis Flow')
    dot.attr(rankdir='TB')  # Top to Bottom direction
    
    # Add nodes
    dot.node('A', 'CSV Data Input\n(basketball_info.csv)')
    dot.node('B', 'Data Processing\n(Chunk Size: 1000)')
    dot.node('C', 'Analysis Phase')
    
    # Analysis sub-nodes
    dot.node('C1', 'Sport Advantages')
    dot.node('C2', 'Web Search\n(Latest Info)')
    dot.node('C3', 'Recommendations')
    
    # Add edges
    dot.edge('A', 'B')
    dot.edge('B', 'C')
    dot.edge('C', 'C1')
    dot.edge('C', 'C2')
    dot.edge('C', 'C3')
    
    # Save the flowchart
    dot.render('basketball_analysis_flow', format='png', cleanup=True)

if __name__ == '__main__':
    create_basketball_analysis_flowchart()
