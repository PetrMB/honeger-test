import { chromium } from 'playwright';
import * as os from 'os';
import * as path from 'path';

const profileDir = path.join(os.homedir(), '.local/share/x-browser-profile');
const claimUrl = process.argv[2] || 'https://moltbook.com/claim/moltbook_claim_hjRb496y9bBuGG7gv26-olHP7XWooGtu';

async function claimMoltbook() {
  console.log('[moltbook-claim] Launching Chrome...');
  
  const browser = await chromium.launchPersistentContext(profileDir, {
    headless: false,
    args: [
      '--disable-blink-features=AutomationControlled',
      '--no-first-run',
      '--no-default-browser-check',
    ],
  });

  const page = await browser.newPage();
  
  console.log(`[moltbook-claim] Navigating to ${claimUrl}...`);
  await page.goto(claimUrl, { waitUntil: 'domcontentloaded' });
  
  // Wait for page to load
  await page.waitForTimeout(3000);
  
  console.log('[moltbook-claim] Looking for claim buttons...');
  
  // Take screenshot first to see current state
  await page.screenshot({ path: '/tmp/moltbook-claim-1.png' });
  
  // Try to find "I've posted the tweet" link (we already posted it via CLI)
  const postedLink = await page.locator('a:has-text("ve posted the tweet"), a:has-text("posted the tweet")').first();
  
  if (await postedLink.isVisible().catch(() => false)) {
    console.log('[moltbook-claim] Clicking "I\'ve posted the tweet" link...');
    await postedLink.click();
    await page.waitForTimeout(5000);
    
    console.log('[moltbook-claim] Claim verification submitted!');
  } else {
    // Try "Post Verification Tweet" button as fallback
    const tweetButton = await page.locator('button:has-text("Post Verification Tweet")').first();
    
    if (await tweetButton.isVisible().catch(() => false)) {
      console.log('[moltbook-claim] Clicking "Post Verification Tweet" button...');
      await tweetButton.click();
      await page.waitForTimeout(10000);
      console.log('[moltbook-claim] Tweet posted and claim submitted!');
    } else {
      console.log('[moltbook-claim] Neither button found - checking page structure...');
    }
  }
  
  // Final screenshot
  await page.screenshot({ path: '/tmp/moltbook-claim-final.png' });
  console.log('[moltbook-claim] Final screenshot saved');
  
  // Keep browser open for 10 seconds to see result
  await page.waitForTimeout(10000);
  
  await browser.close();
}

claimMoltbook().catch(console.error);
