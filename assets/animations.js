// Animations and demo functions

function initializeAnimations() {
    runDemo();
    animateCounter('beforeCost', 0, 52, 1500);
    animateCounter('afterCost', 52, 388, 2000);
}

function runDemo() {
    const output = document.getElementById('demoOutput');
    const command = document.querySelector('.command');
    if (command) command.classList.remove('typing');
    output.textContent = '';

    // Define segments with text and optional color
    const segments = [
        { text: "Scanning Terraform file: main.tf\n\n", color: null },
        { text: "🔍 Analyzing infrastructure changes...\n", color: null },
        { text: "✅ Found 1 cost regression", color: "#10b981" },  // Green for success
        { text: "\n\nFinding #1: ", color: null },
        { text: "High Severity", color: "#ef4444" },  // Red for severity
        { text: "\nResource: aws_instance.web_server\nIssue: Instance type upgraded from t3.medium to t3.xlarge\nImpact: ", color: null },
        { text: "+$150/month (+300% cost increase)", color: "#ef4444" },  // Red for cost increase
        { text: "\nRecommendation: Consider t3.large for better cost-efficiency\n\nTotal potential savings: ", color: null },
        { text: "$150/month", color: "#10b981" }  // Green for savings
    ];

    let segmentIndex = 0;
    let charIndex = 0;
    let currentHTML = '';

    const typeWriter = () => {
        if (segmentIndex < segments.length) {
            const segment = segments[segmentIndex];
            if (charIndex < segment.text.length) {
                currentHTML += segment.color ? `<span style="color: ${segment.color};">${segment.text.charAt(charIndex)}</span>` : segment.text.charAt(charIndex);
                output.innerHTML = currentHTML;
                charIndex++;
                setTimeout(typeWriter, 40);
            } else {
                segmentIndex++;
                charIndex = 0;
                setTimeout(typeWriter, 40);  // Brief pause between segments
            }
        }
    };
    typeWriter();
}

function animateCounter(elementId, start, end, duration) {
    const element = document.getElementById(elementId);
    const startTime = Date.now();

    function update() {
        const elapsed = Date.now() - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const current = Math.floor(start + (end - start) * progress);
        element.textContent = `$${current}`;

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    update();
}

function formatValue(value) {
    if (value >= 1000000) {
        return (value / 1000000).toFixed(1) + 'M';
    } else if (value >= 1000) {
        return (value / 1000).toFixed(1) + 'K';
    }
    return value.toString();
}

function showTrendTooltip(event) {
    const tooltip = document.getElementById('trendTooltip');
    const chart = document.getElementById('trendChart');
    const rect = chart.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    const percentX = x / rect.width;
    const baseCost = 52.43;
    const targetCost = 387.89;
    const estimatedCost = baseCost + (targetCost - baseCost) * percentX;

    tooltip.textContent = `Estimated: $${estimatedCost.toFixed(2)}/month`;
    tooltip.style.left = `${x + 10}px`;
    tooltip.style.top = `${y - 30}px`;
    tooltip.style.display = 'block';
}

function hideTrendTooltip() {
    const tooltip = document.getElementById('trendTooltip');
    tooltip.style.display = 'none';
}

// Initialize Mermaid click handlers
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        const mappingNodes = document.querySelectorAll('#mappingChart .node');
        mappingNodes.forEach(node => {
            node.style.cursor = 'pointer';
            node.addEventListener('click', function() {
                const label = this.textContent;
                alert(`Resource: ${label}\nClick for detailed analysis (feature coming soon)`);
            });
        });
    }, 1000);
});