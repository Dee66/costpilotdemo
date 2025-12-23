const puppeteer = require('puppeteer');
const { PuppeteerScreenRecorder } = require('puppeteer-screen-recorder');

(async () => {
  const browser = await puppeteer.launch({
    headless: false,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-web-security', '--disable-features=VizDisplayCompositor'],
    executablePath: '/usr/bin/google-chrome' // Force Chrome
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 2 }); // Higher resolution for better quality

  // Set zoom to 100% to match screenshot quality
  await page.evaluate(() => {
    document.body.style.zoom = '1';
  });

  const filePath = `file://${__dirname}/index.html`;
  await page.goto(filePath);

  // Wait for ROI calculator to load
  await page.waitForSelector('#roi-calculator');

  // Scroll to ROI section
  await page.evaluate(() => {
    document.getElementById('roi-calculator').scrollIntoView({
      behavior: 'smooth',
      block: 'center'
    });
  });

  // Wait for scroll to complete
  await page.waitForTimeout(1000);

  // Configure recorder with high quality settings
  const recorder = new PuppeteerScreenRecorder(page, {
    fps: 30,
    bitrate: 8000 // Higher bitrate for better quality
  });
  await recorder.start('./video_assets/final/ROIDemo.mp4');

  // Animate sliders with realistic delays
  await animateSlider(page, 'monthlySpend', 0, 15000, 1000);  // $0 to $15k over 1s
  await page.waitForTimeout(250);

  await animateSlider(page, 'wastePercent', 15, 30, 750);   // 15% to 30% over 0.75s  
  await page.waitForTimeout(250);

  await animateSlider(page, 'detectionRate', 95, 85, 500);  // 95% to 85% over 0.5s
  await page.waitForTimeout(250);

  await animateSlider(page, 'monthlySpend', 15000, 25000, 750); // $15k to $25k over 0.75s
  await page.waitForTimeout(1000); // Pause to show final results
  await recorder.stop();
  await browser.close();

  console.log('ROI demo recording saved as video_assets/final/ROIDemo.mp4');
})();

// Helper function to animate slider values smoothly
async function animateSlider(page, sliderId, startValue, endValue, duration) {
  const steps = 50;
  const stepDuration = duration / steps;
  const stepSize = (endValue - startValue) / steps;

  for (let i = 0; i <= steps; i++) {
    const currentValue = Math.round(startValue + (stepSize * i));
    await page.evaluate((id, value) => {
      const slider = document.getElementById(id);
      slider.value = value;
      slider.dispatchEvent(new Event('input', { bubbles: true }));
    }, sliderId, currentValue);

    await page.waitForTimeout(stepDuration);
  }
}