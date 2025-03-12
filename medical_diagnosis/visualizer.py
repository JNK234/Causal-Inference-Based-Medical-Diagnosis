"""
Visualization module for creating interactive visualizations of medical diagnosis data.
"""
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import re
import tempfile
import os
import base64
from io import BytesIO

class Visualizer:
    """
    Creates visualizations for medical diagnosis data including causal graphs,
    treatment comparisons, and other visual representations.
    """
    
    def __init__(self):
        """Initialize the visualizer."""
        pass
    
    def create_causal_graph(self, causal_links_text):
        """
        Create a causal graph visualization from causal links text.
        
        Args:
            causal_links_text (str): Text containing causal links
            
        Returns:
            matplotlib.figure.Figure: The causal graph figure
        """
        # Parse causal links from text
        links = self._parse_causal_links(causal_links_text)
        
        # Create a directed graph
        G = nx.DiGraph()
        
        # Add nodes and edges
        for link in links:
            G.add_edge(link['cause'], link['effect'])
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Set up the layout
        pos = nx.spring_layout(G, seed=42)
        
        # Draw nodes with different colors based on type
        node_colors = []
        for node in G.nodes():
            node_type = self._determine_node_type(node)
            node_colors.append(self._get_color_for_type(node_type))
        
        # Draw the graph
        nx.draw_networkx_nodes(G, pos, node_size=700, node_color=node_colors, alpha=0.8, ax=ax)
        nx.draw_networkx_edges(G, pos, width=2, alpha=0.7, edge_color='gray', arrows=True, ax=ax)
        nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold', ax=ax)
        
        # Set title and remove axis
        plt.title("Causal Relationships", fontsize=16)
        plt.axis('off')
        
        return fig
    
    def _parse_causal_links(self, causal_links_text):
        """
        Parse causal links from text.
        
        Args:
            causal_links_text (str): Text containing causal links
            
        Returns:
            list: List of dictionaries with cause and effect
        """
        links = []
        
        # Look for patterns like "X → Y" or "X -> Y"
        arrow_pattern = r'([^→\n]+)(?:→|->)([^→\n]+)'
        matches = re.finditer(arrow_pattern, causal_links_text)
        
        for match in matches:
            cause = match.group(1).strip()
            effect = match.group(2).strip()
            if cause and effect:
                links.append({
                    'cause': cause,
                    'effect': effect
                })
        
        return links
    
    def _determine_node_type(self, node_text):
        """
        Determine the type of node based on text.
        
        Args:
            node_text (str): The node text
            
        Returns:
            str: The node type
        """
        node_lower = node_text.lower()
        
        # Simple heuristic - would need to be enhanced for real-world use
        if any(term in node_lower for term in ['pain', 'fever', 'nausea', 'vomiting', 'bleeding', 'cough', 'headache']):
            return 'symptom'
        elif any(term in node_lower for term in ['disease', 'syndrome', 'disorder', 'infection', 'failure', 'cancer']):
            return 'condition'
        elif any(term in node_lower for term in ['test', 'scan', 'x-ray', 'mri', 'ct', 'ultrasound', 'biopsy']):
            return 'diagnostic'
        elif any(term in node_lower for term in ['medication', 'drug', 'therapy', 'treatment', 'surgery']):
            return 'treatment'
        else:
            return 'other'
    
    def _get_color_for_type(self, node_type):
        """
        Get color for node type.
        
        Args:
            node_type (str): The node type
            
        Returns:
            str: The color for the node type
        """
        colors = {
            'symptom': '#FF6B6B',  # Red
            'condition': '#4ECDC4',  # Teal
            'diagnostic': '#FFD166',  # Yellow
            'treatment': '#6A0572',  # Purple
            'other': '#C7F9CC'  # Light green
        }
        return colors.get(node_type, '#CCCCCC')  # Default gray
    
    def create_treatment_comparison(self, treatment_plan_text):
        """
        Create a treatment comparison visualization.
        
        Args:
            treatment_plan_text (str): Text containing treatment plan
            
        Returns:
            matplotlib.figure.Figure: The treatment comparison figure
        """
        # Parse treatments from text
        treatments = self._parse_treatments(treatment_plan_text)
        
        if not treatments:
            # Create empty figure with message if no treatments found
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.text(0.5, 0.5, "No treatment data found for visualization", 
                    horizontalalignment='center', verticalalignment='center',
                    transform=ax.transAxes, fontsize=14)
            ax.axis('off')
            return fig
        
        # Create DataFrame
        df = pd.DataFrame(treatments)
        
        # Sort by effectiveness
        df = df.sort_values('effectiveness', ascending=False)
        
        # Create bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.barh(df['name'], df['effectiveness'], color=df['color'])
        
        # Add category labels
        for i, bar in enumerate(bars):
            ax.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2, 
                    df['category'].iloc[i], va='center')
        
        # Set labels and title
        ax.set_xlabel('Effectiveness')
        ax.set_title('Treatment Effectiveness Comparison')
        
        # Set y-axis limits
        ax.set_xlim(0, 1.2)
        
        return fig
    
    def _parse_treatments(self, treatment_plan_text):
        """
        Parse treatments from treatment plan text.
        
        Args:
            treatment_plan_text (str): Text containing treatment plan
            
        Returns:
            list: List of dictionaries with treatment information
        """
        treatments = []
        
        # Look for treatment categorization patterns
        causal_pattern = r'([^–\n]+)–\s*✅\s*Causal Treatment'
        preventative_pattern = r'([^–\n]+)–\s*✅\s*Preventative Treatment'
        symptomatic_pattern = r'([^–\n]+)–\s*❌\s*Symptomatic Treatment'
        
        # Find all matches
        causal_matches = re.finditer(causal_pattern, treatment_plan_text)
        preventative_matches = re.finditer(preventative_pattern, treatment_plan_text)
        symptomatic_matches = re.finditer(symptomatic_pattern, treatment_plan_text)
        
        # Process causal treatments
        for match in causal_matches:
            name = match.group(1).strip()
            if name:
                treatments.append({
                    'name': name,
                    'category': 'Causal',
                    'effectiveness': 0.9,  # Assumed high effectiveness
                    'color': '#4CAF50'  # Green
                })
        
        # Process preventative treatments
        for match in preventative_matches:
            name = match.group(1).strip()
            if name:
                treatments.append({
                    'name': name,
                    'category': 'Preventative',
                    'effectiveness': 0.7,  # Assumed medium effectiveness
                    'color': '#2196F3'  # Blue
                })
        
        # Process symptomatic treatments
        for match in symptomatic_matches:
            name = match.group(1).strip()
            if name:
                treatments.append({
                    'name': name,
                    'category': 'Symptomatic',
                    'effectiveness': 0.5,  # Assumed lower effectiveness
                    'color': '#FFC107'  # Yellow
                })
        
        # If no treatments found with the pattern, try a simpler approach
        if not treatments:
            # Look for numbered treatments
            treatment_pattern = r'\d+\.\s*([^:\n]+)'
            matches = re.finditer(treatment_pattern, treatment_plan_text)
            
            for match in matches:
                name = match.group(1).strip()
                if name:
                    # Determine category based on keywords
                    category = 'Other'
                    effectiveness = 0.6
                    color = '#9C27B0'  # Purple
                    
                    name_lower = name.lower()
                    if any(term in name_lower for term in ['surgery', 'removal', 'repair', 'transplant']):
                        category = 'Causal'
                        effectiveness = 0.9
                        color = '#4CAF50'  # Green
                    elif any(term in name_lower for term in ['prevent', 'prophylactic', 'reduce risk']):
                        category = 'Preventative'
                        effectiveness = 0.7
                        color = '#2196F3'  # Blue
                    elif any(term in name_lower for term in ['pain', 'symptom', 'relief', 'comfort']):
                        category = 'Symptomatic'
                        effectiveness = 0.5
                        color = '#FFC107'  # Yellow
                    
                    treatments.append({
                        'name': name,
                        'category': category,
                        'effectiveness': effectiveness,
                        'color': color
                    })
        
        return treatments
    
    def get_legend_html(self):
        """
        Get HTML for the node type legend.
        
        Returns:
            str: HTML for the legend
        """
        legend_html = """
        <div style="background-color: #f9f9f9; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
            <h4 style="margin-top: 0;">Node Types</h4>
            <div style="display: flex; flex-wrap: wrap;">
                <div style="margin-right: 20px; display: flex; align-items: center;">
                    <div style="width: 15px; height: 15px; background-color: #FF6B6B; border-radius: 50%; margin-right: 5px;"></div>
                    <span>Symptom</span>
                </div>
                <div style="margin-right: 20px; display: flex; align-items: center;">
                    <div style="width: 15px; height: 15px; background-color: #4ECDC4; border-radius: 50%; margin-right: 5px;"></div>
                    <span>Condition</span>
                </div>
                <div style="margin-right: 20px; display: flex; align-items: center;">
                    <div style="width: 15px; height: 15px; background-color: #FFD166; border-radius: 50%; margin-right: 5px;"></div>
                    <span>Diagnostic</span>
                </div>
                <div style="margin-right: 20px; display: flex; align-items: center;">
                    <div style="width: 15px; height: 15px; background-color: #6A0572; border-radius: 50%; margin-right: 5px;"></div>
                    <span>Treatment</span>
                </div>
                <div style="display: flex; align-items: center;">
                    <div style="width: 15px; height: 15px; background-color: #C7F9CC; border-radius: 50%; margin-right: 5px;"></div>
                    <span>Other</span>
                </div>
            </div>
        </div>
        """
        return legend_html
    
    def fig_to_base64(self, fig):
        """
        Convert matplotlib figure to base64 string.
        
        Args:
            fig (matplotlib.figure.Figure): The figure to convert
            
        Returns:
            str: Base64 encoded string of the figure
        """
        buf = BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        return img_str
