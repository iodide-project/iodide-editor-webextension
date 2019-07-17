## Steps to install

### Python dependencies

* pip install [dpallot websocket library](https://github.com/dpallot/simple-websocket-server/blob/master/SimpleWebSocketServer/SimpleWebSocketServer.py)
    * ```pip install SimpleWebSocketServer```

### Development Notes

If the repository has been cloned, nvim can be started from this directory with the ```nvim -u init.vim```, and then the ```:UpdateRemotePlugins``` to follow

### Plugin manager

* using junegunn vimplug
    * add ```Plug 'https://gitlab.com/debyly/iodide-vim-communicator.git'``` to vim-plug block
* run ```:PlugInstall```
* run ```:UpdateRemotePlugins```
* Open a new neovim editor
* ```:StartComm``` is an available command to setup a websocket connector to the Iodide notebook communicating changes in the editor with the screen

**Note, ```:StartComm``` should be executed before the iodide notebook is loaded**
