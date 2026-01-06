// ROI Calculator functionality

function initROICalculator() {
    const monthlySpendSlider = document.getElementById('monthlySpend');
    const wastePercentSlider = document.getElementById('wastePercent');
    const detectionRateSlider = document.getElementById('detectionRate');

    const monthlySpendValue = document.getElementById('monthlySpendValue');
    const wastePercentValue = document.getElementById('wastePercentValue');
    const detectionRateValue = document.getElementById('detectionRateValue');

    const annualSavings = document.getElementById('annualSavings');
    const netBenefit = document.getElementById('netBenefit');
    const roiValue = document.getElementById('roiValue');

    function updateCalculations() {
        const monthlySpend = parseInt(monthlySpendSlider.value);
        const wastePercent = parseInt(wastePercentSlider.value) / 100;
        const detectionRate = parseInt(detectionRateSlider.value) / 100;

        // Update display values
        monthlySpendValue.textContent = `$${monthlySpend.toLocaleString()}`;
        wastePercentValue.textContent = `${wastePercentSlider.value}%`;
        detectionRateValue.textContent = `${detectionRateSlider.value}%`;

        // Update slider progress indicators
        const monthlySpendProgress = ((monthlySpend - 0) / (20000 - 0)) * 180;
        const wastePercentProgress = ((parseInt(wastePercentSlider.value) - 5) / (50 - 5)) * 180;
        const detectionRateProgress = ((parseInt(detectionRateSlider.value) - 80) / (99 - 80)) * 180;

        monthlySpendSlider.parentElement.style.setProperty('--progress-height', `${monthlySpendProgress}px`);
        wastePercentSlider.parentElement.style.setProperty('--progress-height', `${wastePercentProgress}px`);
        detectionRateSlider.parentElement.style.setProperty('--progress-height', `${detectionRateProgress}px`);

        // Calculate annual savings
        const savings = monthlySpend * wastePercent * detectionRate * 12;
        const costPilotCost = 348; // Annual cost

        // Calculate net benefit and ROI
        const benefit = savings - costPilotCost;
        const roi = (benefit / costPilotCost) * 100;

        // Update results
        annualSavings.textContent = `$${Math.round(savings).toLocaleString()}`;
        netBenefit.textContent = `$${Math.round(benefit).toLocaleString()}`;
        roiValue.textContent = `${Math.round(roi)}%`;
    }

    // Add event listeners
    monthlySpendSlider.addEventListener('input', updateCalculations);
    wastePercentSlider.addEventListener('input', updateCalculations);
    detectionRateSlider.addEventListener('input', updateCalculations);

    // Initial calculation
    updateCalculations();
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', initROICalculator);