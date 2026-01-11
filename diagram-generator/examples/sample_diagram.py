import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

def create_claims_ai_architecture():
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Colors
    orange = '#FF8C00'
    blue = '#4169E1'
    light_blue = '#E6F3FF'
    light_orange = '#FFF4E6'
    light_purple = '#F0E6FF'
    purple = '#9932CC'

    # Title
    ax.text(8, 9.3, 'Claims AI Target Architecture', fontsize=20, fontweight='bold', 
            ha='center', color='#333333')

    # Calculate positions for perfect grid alignment
    start_x = 0.5
    total_width = 15
    
    # Top row - 4 equal boxes
    top_box_width = total_width / 4
    top_y = 7.3
    top_height = 1.7
 #-----------------------------------------------------------#
    # Row 1: Agentic AI Portals & UI
    ax.add_patch(FancyBboxPatch((start_x, top_y), top_box_width, top_height, 
                               boxstyle="round,pad=0.3", facecolor=light_blue, 
                               edgecolor=blue, linewidth=2.5))
    ax.text(start_x + top_box_width/2, top_y + top_height/2, 'Agentic AI Portals & UI', 
            fontsize=11, fontweight='bold', ha='center', va='center', color=blue)

    # Row 1: Agentic AI Data platforms
    ax.add_patch(FancyBboxPatch((start_x + top_box_width, top_y), top_box_width, top_height, 
                               boxstyle="round,pad=0.3", facecolor=light_orange, 
                               edgecolor=orange, linewidth=2.5))
    ax.text(start_x + top_box_width + top_box_width/2, top_y + top_height/2, 
            'Agentic AI Data platforms', fontsize=11, fontweight='bold', 
            ha='center', va='center', color=orange)

    # Row 1: Agentic AI Solution
    ax.add_patch(FancyBboxPatch((start_x + 2*top_box_width, top_y), top_box_width, top_height, 
                               boxstyle="round,pad=0.3", facecolor=light_blue, 
                               edgecolor=blue, linewidth=2.5))
    ax.text(start_x + 2*top_box_width + top_box_width/2, top_y + top_height/2, 
            'Agentic AI Solution', fontsize=11, fontweight='bold', 
            ha='center', va='center', color=blue)

    # Row 1: LLM Providers
    ax.add_patch(FancyBboxPatch((start_x + 3*top_box_width, top_y), top_box_width, top_height, 
                               boxstyle="round,pad=0.3", facecolor=light_orange, 
                               edgecolor=orange, linewidth=2.5))
    ax.text(start_x + 3*top_box_width + top_box_width/2, top_y + top_height/2, 
            'LLM Providers', fontsize=11, fontweight='bold', 
            ha='center', va='center', color=orange)

#-----------------------------------------------------------#

    # Middle row - 3 equal boxes
    mid_box_width = total_width / 3.5
    mid_y = 5.3
    mid_height = 1.6

    # Row 2: Agent Usage
    ax.add_patch(FancyBboxPatch((start_x, mid_y), mid_box_width, mid_height, 
                               boxstyle="round,pad=0.3", facecolor=light_blue, 
                               edgecolor=blue, linewidth=2.5))
    ax.text(start_x + mid_box_width/2, mid_y + mid_height/2, 'Agent Usage', 
            fontsize=11, fontweight='bold', ha='center', va='center', color=blue)

    # Row 2: Agent Security
    ax.add_patch(FancyBboxPatch((start_x + mid_box_width, mid_y), mid_box_width, mid_height, 
                               boxstyle="round,pad=0.3", facecolor=light_orange, 
                               edgecolor=orange, linewidth=2.5))
    ax.text(start_x + mid_box_width + mid_box_width/2, mid_y + mid_height/2, 
            'Agent Security', fontsize=11, fontweight='bold', 
            ha='center', va='center', color=orange)

    # Row 2: Observability
    ax.add_patch(FancyBboxPatch((start_x + 2*mid_box_width, mid_y), mid_box_width, mid_height, 
                               boxstyle="round,pad=0.3", facecolor=light_blue, 
                               edgecolor=blue, linewidth=2.5))
    ax.text(start_x + 2*mid_box_width + mid_box_width/2, mid_y + mid_height/2, 
            'Observability', fontsize=11, fontweight='bold', 
            ha='center', va='center', color=blue)

    # SDLC / Deployment - single box on left
    sdlc_y = 3.3
    sdlc_height = 1.7
    sdlc_width = mid_box_width

    ax.add_patch(FancyBboxPatch((start_x, sdlc_y), sdlc_width, sdlc_height, 
                               boxstyle="round,pad=0.1", facecolor=light_purple, 
                               edgecolor=purple, linewidth=2.5))
    ax.text(start_x + sdlc_width/2, sdlc_y + sdlc_height/2, 'SDLC / Deployment', 
            fontsize=11, fontweight='bold', ha='center', va='center', color=purple)

    # AI Governance - full width bottom box
    gov_y = 1.0
    gov_height = 2.0

    ax.add_patch(FancyBboxPatch((start_x, gov_y), total_width, gov_height, 
                               boxstyle="round,pad=0.1", facecolor='#FFF8E1', 
                               edgecolor=orange, linewidth=2.5))
    ax.text(start_x + total_width/2, gov_y + gov_height/2, 'AI Governance', 
            fontsize=13, fontweight='bold', ha='center', va='center', color=orange)

    plt.tight_layout()
    plt.savefig('claims_ai_architecture_outline.png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.show()
    print("Architecture outline diagram generated successfully!")

if __name__ == "__main__":
    create_claims_ai_architecture()