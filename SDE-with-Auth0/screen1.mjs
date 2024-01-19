"use strict";

// Import necessary modules
import puppeteer from 'puppeteer';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

// Define __filename and __dirname for use with ES6 modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Function to take a screenshot of a given URL
async function takeScreenshot(url, screenshotPath) {
    const browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();
    await page.setViewport({ width: 1200, height: 850, deviceScaleFactor: 1 });
    await page.goto(url, { waitUntil: 'networkidle2' });
    await page.screenshot({ path: screenshotPath });
    await browser.close();
}

// Function to sanitize filenames
function sanitizeFilename(name) {
    return name.replace(/[^a-z0-9]/gi, '_').toLowerCase();
}

// Function to process URLs from a file
async function processProfessorUrls(filePath, departmentName) {
    const fileContent = fs.readFileSync(filePath, 'utf8');
    const lines = fileContent.split('\n');

    let currentProfessorName = '';
    let urlIndex = 0;

    for (const line of lines) {
        if (line.startsWith('http')) {
            const sanitizedProfessorName = sanitizeFilename(currentProfessorName);
            const screenshotPath = path.join(__dirname, departmentName, `${sanitizedProfessorName}_screenshot${urlIndex}.png`);
            console.log(`Capturing screenshot for ${currentProfessorName}: ${line}`);
            await takeScreenshot(line, screenshotPath);
            urlIndex++;
        } else if (line.trim() !== '') {
            currentProfessorName = line;
            urlIndex = 0;
        }
    }

    console.log('All screenshots captured for all professors.');
}

// Get department name and file path from command line arguments
const departmentName = process.argv[2];
const urlFilePath = process.argv[3];

// Process the URLs
processProfessorUrls(urlFilePath, departmentName);