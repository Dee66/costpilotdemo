const puppeteer = require('puppeteer');
const { PuppeteerScreenRecorder } = require('puppeteer-screen-recorder');

(async () => {
  const browser = await puppeteer.launch({ 
    headless: false,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080 });
  
  // Go to the local HTML file
  const filePath = `file://${__dirname}/index.html`;
  await page.goto(filePath);
  
  // Wait for the run button
  await page.waitForSelector('#runBtn');
  
  // Start screen recording
  const recorder = new PuppeteerScreenRecorder(page);
  await recorder.start('./video_assets/final/DemoTerminal.mp4');
  
  // Click the run demo button
  await page.click('#runBtn');
  
  // Wait for the animation to complete (6 seconds)
  await page.waitForTimeout(6000);
  
  // Stop recording
  await recorder.stop();
  
  await browser.close();
  
  console.log('Recording saved as video_assets/final/DemoTerminal.mp4');
})();