const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');
const path = require('path');

let pyProc = null;
const PORT = 5000;

function startServer() {
  const exe = app.isPackaged
    ? path.join(process.resourcesPath, 'monitor_server.exe')
    : path.join(__dirname, 'build', 'monitor_server.exe');
  pyProc = spawn(exe, [], { stdio: 'inherit' });
}

async function waitReady(url, tries = 30) {
  for (let i = 0; i < tries; i++) {
    try { await fetch(url + '/api/stats'); return true; }
    catch { await new Promise(r => setTimeout(r, 500)); }
  }
  return false;
}

async function createWindow() {
  startServer();
  const win = new BrowserWindow({
    width: 1100, height: 760,
    title: 'Agent Monitor',
    autoHideMenuBar: true,
    webPreferences: { contextIsolation: true }
  });
  const url = `http://127.0.0.1:${PORT}`;
  if (await waitReady(url)) win.loadURL(url);
  else win.loadFile(path.join(__dirname, 'index.html'));
}

app.whenReady().then(createWindow);
app.on('window-all-closed', () => {
  if (pyProc) pyProc.kill();
  if (process.platform !== 'darwin') app.quit();
});
app.on('before-quit', () => { if (pyProc) pyProc.kill(); });