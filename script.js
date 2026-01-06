// Main initialization script
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Mermaid diagrams
    mermaid.initialize({ startOnLoad: true, theme: 'default' });
    mermaid.init(undefined, '.mermaid');

    // Initialize components
    initializeAnimations();
    initROICalculator();
    loadFindings();
});