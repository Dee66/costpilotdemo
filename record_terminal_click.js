const puppeteer = require('puppeteer');
const fs = require('fs');
const { exec } = require('child_process');

async function recordTerminalDemoClick() {
    console.log('Starting browser for terminal demo autoplay...');
    const browser = await puppeteer.launch({
        headless: true,
        args: ['--window-size=1920,1080', '--no-sandbox', '--disable-dev-shm-usage', '--disable-web-security', '--disable-features=VizDisplayCompositor', '--font-render-hinting=none']
    });

    const page = await browser.newPage();
    await page.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 1 });

    console.log('Navigating to terminal demo page...');
    await page.goto('file://' + __dirname + '/terminal_demo.html', { waitUntil: 'domcontentloaded' });
    console.log('Page loaded');

    // Wait for page to load and elements to be ready
    await page.waitForSelector('.terminal-window');
    await page.waitForSelector('#demoOutput');
    await page.waitForTimeout(1000);

    // Inject runDemo function if not available
    await page.evaluate(() => {
        if (typeof runDemo === 'undefined') {
            window.runDemo = function() {
                const output = document.getElementById('demoOutput');
                const command = document.querySelector('.command');
                command.classList.remove('typing');
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
            };
        }
    });

    // Call runDemo
    await page.evaluate(() => {
        runDemo();
    });
    // Start capturing immediately

    console.log('Capturing terminal demo animation...');
    const frames = [];
    // Capture 24 frames over 9.5 seconds (one frame every 400ms)
    for (let i = 0; i < 24; i++) {
        const framePath = `./video_assets/final/terminal_click_frame_${String(i + 1).padStart(3, '0')}.png`;

        // Capture full viewport
        await page.screenshot({
            path: framePath
        });
        frames.push(framePath);
        console.log(`Frame ${i + 1}/24 captured`);

        // Wait 400ms between frames
        await page.waitForTimeout(400);
    }

    await browser.close();
    console.log('Browser closed, creating terminal demo video...');

    // Use ffmpeg to combine frames into video
    exec(`ffmpeg -y -framerate 2.5 -i ./video_assets/final/terminal_click_frame_%03d.png -c:v libx264 -r 30 -pix_fmt yuv420p -t 9.5 ./video_assets/final/DemoTerminal_click.mp4`, (error, stdout, stderr) => {
        if (error) {
            console.error(`FFmpeg error: ${error.message}`);
            console.error(`stderr: ${stderr}`);
            return;
        }
        console.log('Terminal demo video created successfully');

        // Clean up frame files
        frames.forEach(frame => {
            if (fs.existsSync(frame)) {
                fs.unlinkSync(frame);
            }
        });
        console.log('Frame files cleaned up');
    });
}

recordTerminalDemoClick().catch(console.error);