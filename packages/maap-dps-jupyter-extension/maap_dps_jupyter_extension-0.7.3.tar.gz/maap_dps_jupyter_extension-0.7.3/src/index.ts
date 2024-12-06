import { JupyterFrontEnd, JupyterFrontEndPlugin, ILayoutRestorer } from '@jupyterlab/application'
import { ICommandPalette, MainAreaWidget, WidgetTracker } from '@jupyterlab/apputils'
import { JUPYTER_EXT } from './constants'
import { ViewJobsReactAppWidget, SubmitJobsReactAppWidget } from './classes/App'
import { reactIcon } from '@jupyterlab/ui-components';
import { ILauncher } from '@jupyterlab/launcher';
import { IStateDB } from '@jupyterlab/statedb';
import { IMainMenu } from '@jupyterlab/mainmenu';
import { Menu } from '@lumino/widgets';


/**
 * The command IDs used by the react-widget plugin.
 */
namespace CommandIDs {
  export const create = 'create-react-widget';
}

const profileId = 'maapsec-extension:IMaapProfile';


// Add 'View Jobs' and 'Submit Jobs' plugins to the jupyter lab 'Jobs' menu
const jobs_menu_plugin: JupyterFrontEndPlugin<void> = {
  id: 'jobs-menu',
  autoStart: true,
  requires: [IMainMenu],
  activate: (app: JupyterFrontEnd, mainMenu: IMainMenu) => {
    const { commands } = app;
    let jobsMenu = new Menu({ commands });
    jobsMenu.id = 'jobs-menu';
    jobsMenu.title.label = 'Jobs';
    [
      JUPYTER_EXT.VIEW_JOBS_OPEN_COMMAND,
      JUPYTER_EXT.SUBMIT_JOBS_OPEN_COMMAND
    ].forEach(command => {
      jobsMenu.addItem({ command });
    });
    mainMenu.addMenu(jobsMenu)
  }
};


// View Jobs plugin
const jobs_view_plugin: JupyterFrontEndPlugin<void> = {
  id: JUPYTER_EXT.VIEW_JOBS_PLUGIN_ID,
  autoStart: true,
  optional: [ILauncher, ICommandPalette, IStateDB, ILayoutRestorer],
  activate: (app: JupyterFrontEnd, 
             launcher: ILauncher, 
             palette: ICommandPalette, 
             state: IStateDB, 
             restorer: ILayoutRestorer) => {

    const { commands } = app;

    let viewJobsWidget: MainAreaWidget<ViewJobsReactAppWidget> | null = null;

    const viewJobsTracker = new WidgetTracker<MainAreaWidget<ViewJobsReactAppWidget>>({
      namespace: 'view-jobs-tracker'
    });

    if (restorer) {
      restorer.restore(viewJobsTracker, {
        command: JUPYTER_EXT.VIEW_JOBS_OPEN_COMMAND,
        name: () => 'view-jobs-tracker'
      });
    }

    const command = JUPYTER_EXT.VIEW_JOBS_OPEN_COMMAND;
    commands.addCommand(command, {
      caption: JUPYTER_EXT.VIEW_JOBS_NAME,
      label: JUPYTER_EXT.VIEW_JOBS_NAME,
      icon: (args) => (args['isPalette'] ? null : reactIcon),
      execute: () => {
        const content = new ViewJobsReactAppWidget(app);
        viewJobsWidget = new MainAreaWidget<ViewJobsReactAppWidget>({ content });
        viewJobsWidget.title.label = JUPYTER_EXT.VIEW_JOBS_NAME;
        viewJobsWidget.title.icon = reactIcon;
        app.shell.add(viewJobsWidget, 'main');

        // Add widget to the tracker so it will persist on browser refresh
        viewJobsTracker.save(viewJobsWidget)
        viewJobsTracker.add(viewJobsWidget)
      },
    });

    palette.addItem({command: JUPYTER_EXT.VIEW_JOBS_OPEN_COMMAND, category: 'MAAP Extensions'});

    if (launcher) {
      launcher.add({
        command,
        category: "MAAP Extensions"
      });
    }

    console.log('JupyterLab MAAP View Jobs extension is activated!');
  },
  
};

// Submit Jobs plugin
const jobs_submit_plugin: JupyterFrontEndPlugin<void> = {
  id: JUPYTER_EXT.SUBMIT_JOBS_PLUGIN_ID,
  autoStart: true,
  optional: [ILauncher, ICommandPalette, IStateDB, ILayoutRestorer],
  activate: (app: JupyterFrontEnd, 
             launcher: ILauncher, 
             palette: ICommandPalette, 
             state: IStateDB, 
             restorer: ILayoutRestorer) => {

    const { commands } = app;

    let submitJobsWidget: MainAreaWidget<SubmitJobsReactAppWidget> | null = null;

    const submitJobsTracker = new WidgetTracker<MainAreaWidget<SubmitJobsReactAppWidget>>({
      namespace: 'submit-jobs-tracker'
    });

    if (restorer) {
      restorer.restore(submitJobsTracker, {
        command: JUPYTER_EXT.SUBMIT_JOBS_OPEN_COMMAND,
        name: () => 'submit-jobs-tracker'
      });
    }

    const command = JUPYTER_EXT.SUBMIT_JOBS_OPEN_COMMAND;

    commands.addCommand(command, {
      caption: JUPYTER_EXT.SUBMIT_JOBS_NAME,
      label: JUPYTER_EXT.SUBMIT_JOBS_NAME,
      icon: (args) => (args['isPalette'] ? null : reactIcon),
      execute: () => {
        const content = new SubmitJobsReactAppWidget("", app);
        submitJobsWidget = new MainAreaWidget<SubmitJobsReactAppWidget>({ content });
        submitJobsWidget.title.label = JUPYTER_EXT.SUBMIT_JOBS_NAME;
        submitJobsWidget.title.icon = reactIcon;
        app.shell.add(submitJobsWidget, 'main');

        // Add widget to the tracker so it will persist on browser refresh
        submitJobsTracker.save(submitJobsWidget)
        submitJobsTracker.add(submitJobsWidget)
      },
    });

    palette.addItem({command: JUPYTER_EXT.SUBMIT_JOBS_OPEN_COMMAND, category: 'MAAP Extensions'});

    if (launcher) {
      launcher.add({
        command,
        category: "MAAP Extensions"
      });
    }

    console.log('JupyterLab MAAP Submit Jobs plugin is activated!');
  }
};

export default [jobs_view_plugin, jobs_menu_plugin, jobs_submit_plugin];
