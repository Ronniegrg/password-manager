"use strict";
/*
 * Copyright (c) 2022, salesforce.com, inc.
 * All rights reserved.
 * Licensed under the BSD 3-Clause license.
 * For full license text, see LICENSE.txt file in the repo root or https://opensource.org/licenses/BSD-3-Clause
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.create = exports.configureAutoUpdate = exports.configureUpdateSites = exports.UPDATE_DISABLED_DEMO = exports.UPDATE_DISABLED_NPM = exports.UPDATE_DISABLED_INSTALLER = void 0;
const os = require("os");
const path = require("path");
const core_1 = require("@oclif/core");
const kit_1 = require("@salesforce/kit");
const ts_types_1 = require("@salesforce/ts-types");
const Debug = require("debug");
const env_1 = require("./util/env");
const debug = Debug('sf');
const envVars = [
    ...new Set([
        ...Object.keys(process.env).filter((e) => e.startsWith('SF_') || e.startsWith('SFDX_')),
        'NODE_OPTIONS',
        env_1.Env.SF_AUTOUPDATE_DISABLE,
        'SF_BINPATH',
        'SF_COMPILE_CACHE',
        env_1.Env.SF_DISABLE_AUTOUPDATE,
        env_1.Env.SF_ENV,
        env_1.Env.SF_INSTALLER,
        env_1.Env.SF_NPM_REGISTRY,
        'SF_REDIRECTED',
        env_1.Env.SF_UPDATE_INSTRUCTIONS,
    ]),
];
exports.UPDATE_DISABLED_INSTALLER = 'Manual and automatic CLI updates have been disabled by setting "SF_AUTOUPDATE_DISABLE=true". ' +
    'To check for a new version, unset that environment variable.';
exports.UPDATE_DISABLED_NPM = 'Use "npm update --global @salesforce/cli" to update npm-based installations.';
exports.UPDATE_DISABLED_DEMO = 'Manual and automatic CLI updates have been disabled in DEMO mode. ' +
    'To check for a new version, unset the environment variable SF_ENV.';
function configureUpdateSites(config, env = env_1.default) {
    const npmRegistry = env.getNpmRegistryOverride();
    if (npmRegistry) {
        // Override config value if set via envar
        (0, kit_1.set)(config, 'pjson.oclif.warn-if-update-available.registry', npmRegistry);
    }
}
exports.configureUpdateSites = configureUpdateSites;
function configureAutoUpdate(envars) {
    if (envars.isDemoMode()) {
        // Disable autoupdates in demo mode
        envars.setAutoupdateDisabled(true);
        envars.setUpdateInstructions(exports.UPDATE_DISABLED_DEMO);
        return;
    }
    if (envars.isInstaller()) {
        envars.normalizeAutoupdateDisabled();
        if (envars.isAutoupdateDisabled()) {
            envars.setUpdateInstructions(exports.UPDATE_DISABLED_INSTALLER);
        }
        return;
    }
    // Not an installer, so this must be running from an npm installation
    if (!envars.isAutoupdateDisabledSet()) {
        // Disable autoupdates if run from an npm install or in local dev, if not explicitly set
        envars.setAutoupdateDisabled(true);
    }
    if (envars.isAutoupdateDisabled()) {
        envars.setUpdateInstructions(exports.UPDATE_DISABLED_NPM);
    }
}
exports.configureAutoUpdate = configureAutoUpdate;
function debugCliInfo(version, channel, env, config) {
    function debugSection(section, items) {
        const pad = 25;
        debug('%s:', section.padStart(pad));
        items.forEach(([name, value]) => debug('%s: %s', name.padStart(pad), value));
    }
    debugSection('OS', [
        ['platform', os.platform()],
        ['architecture', os.arch()],
        ['release', os.release()],
        ['shell', config.shell],
    ]);
    debugSection('NODE', [['version', process.versions.node]]);
    debugSection('CLI', [
        ['version', version],
        ['channel', channel],
        ['bin', config.bin],
        ['data', config.dataDir],
        ['cache', config.cacheDir],
        ['config', config.configDir],
    ]);
    debugSection('ENV', [...envVars].map((key) => [key, env.getString(key, '<not set>')]));
    debugSection('ARGS', process.argv.map((arg, i) => [i.toString(), arg]));
}
function create(version, channel, run, env = env_1.default) {
    core_1.settings.performanceEnabled = true;
    const root = path.resolve(__dirname, '..');
    // eslint-disable-next-line @typescript-eslint/no-var-requires
    const pjson = require(path.resolve(__dirname, '..', 'package.json'));
    const args = process.argv.slice(2);
    return {
        async run() {
            const config = new core_1.Config({
                name: (0, ts_types_1.get)(pjson, 'oclif.bin'),
                root,
                version,
                channel,
            });
            await config.load();
            configureUpdateSites(config, env);
            configureAutoUpdate(env);
            debugCliInfo(version, channel, env, config);
            // Example of how run is used in a test https://github.com/salesforcecli/cli/pull/171/files#diff-1deee0a575599b2df117c280da319f7938aaf6fdb0c04bcdbde769dbf464be69R46
            return run ? run(args, config) : (0, core_1.run)(args, config);
        },
    };
}
exports.create = create;
//# sourceMappingURL=cli.js.map