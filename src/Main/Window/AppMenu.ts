import electron, {
  app,
  Menu,
  MenuItemConstructorOptions,
  shell
} from 'electron';
import {BrowserViewBind} from '../Bind/BrowserViewBind';
import {AppWindow} from './AppWindow';
import {DB} from '../Storage/DB';
import {StreamIPC} from '../../IPC/StreamIPC';
import {GAIPC} from '../../IPC/GAIPC';
import {ConfigStorage} from '../Storage/ConfigStorage';

class _AppMenu {
  private appMenu: Menu;
  private skipReadIssue: number = 0;
  private currentZoom: number = 1;

  async init() {
    if (!this.appMenu) this.buildMainMenu();
    Menu.setApplicationMenu(this.appMenu);
  }

  enableShortcut(enable: boolean) {
    // devtoolが開いてるときは強制的にoffにする
    if (AppWindow.getWindow().webContents.isDevToolsOpened()) enable = false;

    setEnable(enable, this.appMenu)

    function setEnable(enable: boolean, menu: Menu) {
      for (const menuItem of menu.items) {
        // 1文字ショートカットのメニューのon/off
        if (menuItem.accelerator?.length === 1) menuItem.enabled = enable;
        if (menuItem.submenu) setEnable(enable, menuItem.submenu);
      }
    }
  }

  private async quit() {
    GAIPC.eventAppEnd();
    app.exit(0);
  }

  private switchLayout(layout: 'single' | 'two' | 'three') {
    AppWindow.getWindow().webContents.send('switch-layout', layout);
    GAIPC.eventMenu(`layout:${layout}`);
  }

  // target is webview|issues|streams
  private commandWebContents(target: 'app' | 'webview' | 'issues' | 'streams', command: string) {
    // hack
    if (this.skipReadIssue && target === 'issues' && ['next', 'prev'].includes(command)) command = `${command}_with_skip`;

    AppWindow.getWindow().webContents.send(`command-${target}`, {command});

    GAIPC.eventMenu(`${target}:${command}`);
  }

  private zoom(diffFactor: number, abs: boolean) {
    if (abs) {
      this.currentZoom = diffFactor;
    } else {
      this.currentZoom += diffFactor;
    }

    this.currentZoom = Math.max(this.currentZoom, 0.05);

    AppWindow.getWindow().webContents.setZoomFactor(this.currentZoom);
    BrowserViewBind.setZoomFactor(this.currentZoom);

    GAIPC.eventMenu(`zoom:${this.currentZoom}`);
  }

  private openConfigDir() {
    shell.showItemInFolder(ConfigStorage.getConfigPath());
  }

  async vacuum() {
    const notification = new electron.Notification({title: 'SQLite Vacuum', body: 'Running...'});
    notification.show();

    await StreamIPC.stopAllStreams();
    await DB.exec('vacuum');
    await StreamIPC.restartAllStreams();

    notification.close();
  }

  private buildMainMenu() {
    const template: MenuItemConstructorOptions[] = [
      {
        label: "Application",
        submenu: [
          { label: "About Jasper", click: () => this.commandWebContents('app', 'open_about') },
          { type: "separator" },
          { label: "Preferences", accelerator: "CmdOrCtrl+,", click: () => this.commandWebContents('app', 'open_pref') },
          { label: "Update", click: ()=>{electron.shell.openExternal('https://jasperapp.io/release.html')} },
          { type: "separator" },
          { label: 'Services', role: 'services' },
          { type: "separator" },
          { label: 'Hide Jasper', accelerator: 'CmdOrCtrl+H', role: 'hide' },
          { label: 'Hide Others', accelerator: 'Option+CmdOrCtrl+H', role: 'hideOthers' },
          { label: 'Show All', role: 'unhide' },
          { type: "separator" },
          { label: "Quit Jasper", accelerator: "CmdOrCtrl+Q", click: this.quit.bind(this)}
        ]
      },
      {
        label: "Edit",
        submenu: [
          { label: "Undo", accelerator: "CmdOrCtrl+Z", role: "undo" },
          { label: "Redo", accelerator: "Shift+CmdOrCtrl+Z", role: "redo" },
          { type: "separator" },
          { label: "Cut", accelerator: "CmdOrCtrl+X", role: "cut" },
          { label: "Copy", accelerator: "CmdOrCtrl+C", role: "copy" },
          { label: "Paste", accelerator: "CmdOrCtrl+V", role: "paste" },
          { label: "Select All", accelerator: "CmdOrCtrl+A", role: "selectAll" }
        ]
      },
      {
        label: 'View',
        submenu: [
          { label: 'Single Pane', accelerator: 'CmdOrCtrl+1', click: this.switchLayout.bind(this, 'single') },
          { label: 'Two Pane', accelerator: 'CmdOrCtrl+2', click: this.switchLayout.bind(this, 'two') },
          { label: 'Three Pane', accelerator: 'CmdOrCtrl+3', click: this.switchLayout.bind(this, 'three') },
          { type: "separator" },
          { label: 'Full Screen', role: 'togglefullscreen' }
        ]
      },
      {
        label: 'Streams',
        submenu: [
          { label: 'Next Stream', accelerator: 'D', click: this.commandWebContents.bind(this, 'app', 'next_stream')},
          { label: 'Prev Stream', accelerator: 'F', click: this.commandWebContents.bind(this, 'app', 'prev_stream')},
          { type: 'separator' },
          { label: 'LIBRARY', submenu: [
              { label: 'Inbox', accelerator: 'F1', click: this.commandWebContents.bind(this, 'app', 'load_inbox')},
              { label: 'Unread', accelerator: 'F2', click: this.commandWebContents.bind(this, 'app', 'load_unread')},
              { label: 'Open', accelerator: 'F3', click: this.commandWebContents.bind(this, 'app', 'load_open')},
              { label: 'Star', accelerator: 'F4', click: this.commandWebContents.bind(this, 'app', 'load_mark')},
              { label: 'Archive', accelerator: 'F5', click: this.commandWebContents.bind(this, 'app', 'load_archive')}
            ]},
          { label: 'SYSTEM', submenu: [
              { label: 'Me', accelerator: 'F6', click: this.commandWebContents.bind(this, 'app', 'load_me')},
              { label: 'Team', accelerator: 'F7', click: this.commandWebContents.bind(this, 'app', 'load_team')},
              { label: 'Watching', accelerator: 'F8', click: this.commandWebContents.bind(this, 'app', 'load_watching')},
              { label: 'Subscription', accelerator: 'F9', click: this.commandWebContents.bind(this, 'app', 'load_subscription')}
            ]},
          { label: 'STREAMS', submenu: [
              { label: '1st', accelerator: '1', click: this.commandWebContents.bind(this, 'app', 'load_1st')},
              { label: '2nd', accelerator: '2', click: this.commandWebContents.bind(this, 'app', 'load_2nd')},
              { label: '3rd', accelerator: '3', click: this.commandWebContents.bind(this, 'app', 'load_3rd')},
              { label: '4th', accelerator: '4', click: this.commandWebContents.bind(this, 'app', 'load_4th')},
              { label: '5th', accelerator: '5', click: this.commandWebContents.bind(this, 'app', 'load_5th')}
            ]},
          { type: 'separator' },
          { label: 'Restart Streams', accelerator: 'Alt+L', click: () => StreamIPC.restartAllStreams() }
        ]
      },
      {
        label: 'Issues',
        submenu: [
          { label: 'Load Issues', accelerator: '.', click: this.commandWebContents.bind(this, 'issues', 'load') },
          { type: 'separator' },
          { label: 'Next Issue', accelerator: 'J', click: this.commandWebContents.bind(this, 'issues', 'next') },
          { label: 'Prev Issue', accelerator: 'K', click: this.commandWebContents.bind(this, 'issues', 'prev') },
          { label: 'Skip Read(On/Off)', accelerator: 'Y', type: 'checkbox', click: ()=>{ this.skipReadIssue ^= 1 } },
          { type: 'separator' },
          { label: 'Toggle', submenu: [
              { label: 'Read', accelerator: 'I', click: this.commandWebContents.bind(this, 'webview', 'read') },
              { label: 'Star', accelerator: 'S', click: this.commandWebContents.bind(this, 'webview', 'mark') },
              { label: 'Archive', accelerator: 'E', click: this.commandWebContents.bind(this, 'webview', 'archive') }
            ]},
          { type: 'separator' },
          {label: 'Filter', submenu: [
              { label: 'Focus On', accelerator: '/', click: this.commandWebContents.bind(this, 'issues', 'focus_filter') },
              { label: 'Author', accelerator: 'A', click: this.commandWebContents.bind(this, 'issues', 'filter_author') },
              { label: 'Assignee', accelerator: 'N', click: this.commandWebContents.bind(this, 'issues', 'filter_assignee') },
              { label: 'Unread', accelerator: 'U', click: this.commandWebContents.bind(this, 'issues', 'filter_unread') },
              { label: 'Open', accelerator: 'O', click: this.commandWebContents.bind(this, 'issues', 'filter_open') },
              { label: 'Star', accelerator: 'M', click: this.commandWebContents.bind(this, 'issues', 'filter_mark') },
              { label: 'Clear', accelerator: 'C', click: this.commandWebContents.bind(this, 'issues', 'filter_clear') }
            ]},
          { type: 'separator' },
          { label: 'Open with External', accelerator: 'CmdOrCtrl+O', click: this.commandWebContents.bind(this, 'webview', 'export') }
        ]
      },
      {
        label: 'Page',
        submenu: [
          { label: 'Reload', accelerator: 'CmdOrCtrl+R', click: this.commandWebContents.bind(this, 'webview', 'reload') },
          { label: 'Back', accelerator: 'CmdOrCtrl+[', click: this.commandWebContents.bind(this, 'webview', 'back') },
          { label: 'Forward', accelerator: 'CmdOrCtrl+]', click: this.commandWebContents.bind(this, 'webview', 'forward') },
          { type: 'separator' },
          { label: 'Scroll Down', accelerator: 'CmdOrCtrl+J', click: this.commandWebContents.bind(this, 'webview', 'scroll_down') },
          { label: 'Scroll Up', accelerator: 'CmdOrCtrl+K', click: this.commandWebContents.bind(this, 'webview', 'scroll_up') },
          { type: 'separator' },
          { label: 'Open Location', accelerator: 'CmdOrCtrl+L', click: this.commandWebContents.bind(this, 'webview', 'open_location') }
        ]
      },
      {
        label: 'Window', role: 'window',
        submenu: [
          {label: 'Zoom +', accelerator: 'CmdOrCtrl+Plus', click: this.zoom.bind(this, 0.05, false)},
          {label: 'Zoom -', accelerator: 'CmdOrCtrl+-', click: this.zoom.bind(this, -0.05, false)},
          {label: 'Zoom Reset', accelerator: 'CmdOrCtrl+0', click: this.zoom.bind(this, 1, true)},
          { type: "separator" },
          {label: 'Minimize', accelerator: 'CmdOrCtrl+M', role: 'minimize'},
          {label: 'Bring All to Front', role: 'front'}
        ]
      },
      {
        label: 'Help', role: 'help',
        submenu: [
          {label: 'Documentation', submenu: [
              {label: 'Library', click: ()=>{electron.shell.openExternal('https://jasperapp.io/doc.html#library')}},
              {label: 'System', click: ()=>{electron.shell.openExternal('https://jasperapp.io/doc.html#your-issues')}},
              {label: 'Stream', click: ()=>{electron.shell.openExternal('https://jasperapp.io/doc.html#stream')}},
              {label: 'Filter', click: ()=>{electron.shell.openExternal('https://jasperapp.io/doc.html#filter')}},
              {label: 'Sort', click: ()=>{electron.shell.openExternal('https://jasperapp.io/doc.html#sort')}},
              {label: 'Issue', click: ()=>{electron.shell.openExternal('https://jasperapp.io/doc.html#issue')}},
              {label: 'Shortcut Key', click: ()=>{electron.shell.openExternal('https://jasperapp.io/doc.html#shortcut')}}
            ]},
          {label: 'FAQ', click: ()=>{electron.shell.openExternal('https://jasperapp.io/faq.html')}},
          {label: 'Feedback', click: ()=>{electron.shell.openExternal('https://github.com/jasperapp/jasper')}}
        ]
      },
      {
        label: 'Dev',
        submenu: [
          {label: 'DevTools(Main)', click: ()=>{ AppWindow.getWindow().webContents.openDevTools({mode: 'detach'}); }},
          {label: 'DevTools(BrowserView)', click: ()=>{ BrowserViewBind.getWebContents().openDevTools({mode: 'detach'}); }},
          { type: 'separator' },
          {label: 'Open Config Directory', click: this.openConfigDir.bind(this)},
          {label: 'SQLite Vacuum', click: this.vacuum.bind(this)},
        ]
      }
    ];

    this.appMenu = Menu.buildFromTemplate(template);
  }
}

export const AppMenu = new _AppMenu();