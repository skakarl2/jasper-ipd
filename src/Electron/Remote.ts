import {remote} from 'electron';
import {DB} from '../DB/DB';
import {BrowserViewProxy} from '../Main/BrowserViewProxy';
import {Config} from '../Main/Config';
import {GA} from '../Util/GA';
import {DateConverter} from '../Util/DateConverter';
import {StreamEmitter} from '../Stream/StreamEmitter';
import {StreamLauncher} from '../Stream/StreamLauncher';
import {SystemStreamLauncher} from '../Stream/SystemStreamLauncher';
import {GitHubClient} from '../GitHub/GitHubClient';
import {IssuesTable} from '../DB/IssuesTable';
import {StreamsIssuesTable} from '../DB/StreamsIssuesTable';
import {Bootstrap} from '../Main/Bootstrap';

export const RemoteDB: typeof DB = remote.require('./DB/DB').DB;
export const RemoteLogger = remote.require('color-logger').default;
export const RemoteStreamLauncher: typeof StreamLauncher = remote.require('./Stream/StreamLauncher').StreamLauncher;
export const RemoteSystemStreamLauncher: typeof SystemStreamLauncher = remote.require('./Stream/SystemStreamLauncher').SystemStreamLauncher;
export const RemoteStreamEmitter: typeof StreamEmitter = remote.require('./Stream/StreamEmitter').StreamEmitter;
export const RemoteConfig: typeof Config = remote.require('./Main/Config').Config;
export const RemoteGitHubClient: typeof GitHubClient = remote.require('./GitHub/GitHubClient').GitHubClient;
export const RemoteIssuesTable: typeof IssuesTable = remote.require('./DB/IssuesTable').IssuesTable;
export const RemoteStreamsIssuesTable: typeof StreamsIssuesTable = remote.require('./DB/StreamsIssuesTable').StreamsIssuesTable;
export const RemoteGA: typeof GA = remote.require('./Util/GA').GA;
export const RemoteDateConverter: typeof DateConverter = remote.require('./Util/DateConverter').DateConverter;
export const RemoteBrowserViewProxy: typeof BrowserViewProxy = remote.require('./Main/BrowserViewProxy').BrowserViewProxy;
export const RemoteBootstrap: typeof Bootstrap = remote.require('./Main/Bootstrap').Bootstrap;
