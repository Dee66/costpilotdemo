// Findings management functions

function loadFindings() {
    renderHardcodedFindings();
}

function renderFindings(findings) {
    console.log('renderFindings called with', findings.length, 'findings');
    const container = document.getElementById('findingsContainer');
    console.log('Container before render:', container.innerHTML.length, 'characters');
    container.innerHTML = findings.map(createFindingCard).join('');
    console.log('Container after render:', container.innerHTML.length, 'characters');

    // Add click event listeners
    const cards = container.querySelectorAll('.finding-card');
    cards.forEach((card, index) => {
        card.addEventListener('click', () => {
            card.classList.toggle('expanded');
        });
        // Expand the first finding by default to show the image
        if (index === 0) {
            card.classList.add('expanded');
        }
    });
}

function createFindingCard(finding) {
    console.log('Creating card for finding:', finding.finding_id);
    const html = `
        <div class="finding-card high">
            <div class="finding-header">
                <div class="finding-title">🔴 ${finding.resource_address || 'Unknown'}</div>
                <span class="severity-badge high">high</span>
            </div>
            <div class="finding-detail"><strong>ID:</strong> ${finding.finding_id || 'N/A'}</div>
            <div class="expand-hint">▼ Click to see full analysis</div>
            <div class="finding-details-expanded">
                <div style="margin-top: 1.5rem;">
                    <img src="./visual_assets/screenshots/FindingOne.png" alt="Finding Analysis" style="width: 100%; max-width: 600px; border-radius: 8px; border: 1px solid var(--border);">
                </div>
            </div>
        </div>
    `;
    console.log('Generated HTML length:', html.length);
    return html;
}

function renderHardcodedFindings() {
    console.log('renderHardcodedFindings called');
    // Fallback hardcoded findings (same as before)
    const container = document.getElementById('findingsContainer');
    container.innerHTML = `
        <div class="finding-card high">
            <div class="finding-header">
                <div class="finding-title">🔴 aws_launch_template.main</div>
                <span class="severity-badge high">high</span>
            </div>
            <div class="finding-detail"><strong>Type:</strong> aws_launch_template (compute)</div>
            <div class="finding-detail"><strong>Change:</strong> instance_type from t3.micro to t3.xlarge</div>
            <div class="finding-detail"><strong>Impact:</strong> 16x cost increase</div>

            <div class="expand-hint">▼ Click to see full analysis</div>

            <div class="finding-details-expanded">
                <div class="rationale">
                    <strong>Analysis:</strong><br>
                    This instance type change from t3.micro to t3.xlarge represents a significant cost increase due to higher vCPU and memory allocation.
                </div>

                <div style="margin-top: 1rem;">
                    <strong style="display: block; margin-bottom: 0.5rem;">Triggered Rules:</strong>
                    <span class="policy-tag">cost-optimization</span><span class="policy-tag">instance-sizing</span>
                </div>

                <div style="margin-top: 1rem;">
                    <strong>Cost Impact Likelihood:</strong>
                    <span style="color: var(--danger); font-weight: 600; text-transform: uppercase;">high</span>
                </div>

                <div style="margin-top: 1rem;">
                    <strong>Regression Type:</strong> infrastructure change
                </div>
            </div>
        </div>
        <div class="finding-card medium">
            <div class="finding-header">
                <div class="finding-title">🟡 aws_ebs_volume.data</div>
                <span class="severity-badge medium">medium</span>
            </div>
            <div class="finding-detail"><strong>Type:</strong> aws_ebs_volume (storage)</div>
            <div class="finding-detail"><strong>Change:</strong> size from 20GB to 200GB</div>
            <div class="finding-detail"><strong>Impact:</strong> 10x cost increase</div>

            <div class="expand-hint">▼ Click to see full analysis</div>

            <div class="finding-details-expanded">
                <div class="rationale">
                    <strong>Analysis:</strong><br>
                    EBS volume size increase from 20GB to 200GB significantly impacts storage costs without proportional benefit.
                </div>

                <div style="margin-top: 1rem;">
                    <strong style="display: block; margin-bottom: 0.5rem;">Triggered Rules:</strong>
                    <span class="policy-tag">storage-optimization</span>
                </div>

                <div style="margin-top: 1rem;">
                    <strong>Cost Impact Likelihood:</strong>
                    <span style="color: var(--warning); font-weight: 600; text-transform: uppercase;">medium</span>
                </div>

                <div style="margin-top: 1rem;">
                    <strong>Regression Type:</strong> configuration drift
                </div>
            </div>
        </div>
        <div class="finding-card high">
            <div class="finding-header">
                <div class="finding-title">🔴 aws_s3_bucket.logs</div>
                <span class="severity-badge high">high</span>
            </div>
            <div class="finding-detail"><strong>Type:</strong> aws_s3_bucket (storage)</div>
            <div class="finding-detail"><strong>Change:</strong> lifecycle rules removed</div>
            <div class="finding-detail"><strong>Impact:</strong> Unlimited storage costs</div>

            <div class="expand-hint">▼ Click to see full analysis</div>

            <div class="finding-details-expanded">
                <div class="rationale">
                    <strong>Analysis:</strong><br>
                    Removing lifecycle rules from S3 bucket will result in indefinite storage of logs, leading to escalating costs over time.
                </div>

                <div style="margin-top: 1rem;">
                    <strong style="display: block; margin-bottom: 0.5rem;">Triggered Rules:</strong>
                    <span class="policy-tag">storage-lifecycle</span><span class="policy-tag">cost-optimization</span>
                </div>

                <div style="margin-top: 1rem;">
                    <strong>Cost Impact Likelihood:</strong>
                    <span style="color: var(--danger); font-weight: 600; text-transform: uppercase;">high</span>
                </div>

                <div style="margin-top: 1rem;">
                    <strong>Regression Type:</strong> configuration removal
                </div>
            </div>
        </div>
        <div class="finding-card medium">
            <div class="finding-header">
                <div class="finding-title">🟡 aws_cloudwatch_log_group.app</div>
                <span class="severity-badge medium">medium</span>
            </div>
            <div class="finding-detail"><strong>Type:</strong> aws_cloudwatch_log_group (monitoring)</div>
            <div class="finding-detail"><strong>Change:</strong> retention_in_days from 30 to 0</div>
            <div class="finding-detail"><strong>Impact:</strong> Never expiring logs</div>

            <div class="expand-hint">▼ Click to see full analysis</div>

            <div class="finding-details-expanded">
                <div class="rationale">
                    <strong>Analysis:</strong><br>
                    Setting retention to 0 (never expire) on CloudWatch logs will accumulate costs indefinitely as logs grow over time.
                </div>

                <div style="margin-top: 1rem;">
                    <strong style="display: block; margin-bottom: 0.5rem;">Triggered Rules:</strong>
                    <span class="policy-tag">log-retention</span><span class="policy-tag">cost-optimization</span>
                </div>

                <div style="margin-top: 1rem;">
                    <strong>Cost Impact Likelihood:</strong>
                    <span style="color: var(--warning); font-weight: 600; text-transform: uppercase;">medium</span>
                </div>

                <div style="margin-top: 1rem;">
                    <strong>Regression Type:</strong> configuration change
                </div>
            </div>
        </div>
    `;

    // Add click event listeners
    const cards = container.querySelectorAll('.finding-card');
    cards.forEach((card, index) => {
        const expandHint = card.querySelector('.expand-hint');
        card.addEventListener('click', () => {
            card.classList.toggle('expanded');
            // Update the hint text based on expanded state
            if (card.classList.contains('expanded')) {
                expandHint.textContent = '▲ Click to collapse';
            } else {
                expandHint.textContent = '▼ Click to see full analysis';
            }
        });
        // Expand the first finding by default to show the image
        if (index === 0) {
            card.classList.add('expanded');
            expandHint.textContent = '▲ Click to collapse';
        }
    });
}