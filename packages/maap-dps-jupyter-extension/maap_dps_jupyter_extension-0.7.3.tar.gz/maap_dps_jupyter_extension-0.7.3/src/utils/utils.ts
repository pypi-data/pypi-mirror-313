import { Notification } from "@jupyterlab/apputils"
import { IStateDB } from '@jupyterlab/statedb';
import { JUPYTER_EXT } from "../constants";

/**
 * Converts seconds to a human-readable string using this format:
 * HHh MMm SSs
 * 
 * @param seconds - string
 */
export const secondsToReadableString = (seconds: string) => {
    let d = Number(seconds)
    if (isNaN(d)) {
        return "";
    }

    let h = Math.floor(d / 3600)
    let m = Math.floor(d % 3600 / 60)
    let s = Math.floor(d % 3600 % 60)
    var str = h + 'h ' + m + 'm ' + s + 's '
    return str
}


export const getProducts = (products: []) => {

    // if (products.length !> 0) {
    //     return ""
    // }

    const urls = new Set()
    // note that currently there should only be one element in products
    products.forEach((product: any) => {
        product["urls"].forEach((url) => {
            urls.add(url)
        })
    })

    let urls_str = Array.from(urls).join('\r\n')
    return urls_str
}

/**
 * If there is more than one product folder path, print to console because that shouldn't be the case and we will need 
 * to revisit if it is. Only take the first folder path if that is the case though. 
 * @param products list of products - should only be be one because only one element in products_staged right now
 * @returns A single folder path
 */
export const getProductFolderPath = (products: []) => {
    let productFolderPaths = new Set();
    products.forEach((product: any) => {
        productFolderPaths.add(product["product_folder_path"])
    })

    let productFolderPathsArr = Array.from(productFolderPaths);
    if (productFolderPathsArr.length > 1) {
        console.error("Folder path length was "+productFolderPathsArr.length+". We are only looking at the first element.");
    }

    return productFolderPathsArr.length? productFolderPathsArr[0]: null;
}


export var getUserInfo = function (callback) {
    window.parent._keycloak.loadUserInfo().success(function (profile) {
        callback(profile);

    }).error(function () {
        return "error";
    });
};


/*export async function getUsernameToken(state: IStateDB, profileId: string, callback) {
    let uname: string = DEFAULT_USERNAME
    let ticket: string = '';

    let ade_server = ''
    let response = getEnvironmentInfo()

    response.then((data) => {
        console.log("ADE SERVER: ", data["ade_server"])
        ade_server = data["ade_server"]
    }).finally(() => {
        if ("https://" + ade_server === document.location.origin) {
            getUserInfo(function (profile: any) {
                if (profile['cas:username'] === undefined) {
                    Notification.error("Get profile failed.", { autoClose: false });
                } else {
                    console.log("Getting username...")
                    uname = profile['cas:username'];
                    ticket = profile['proxyGrantingTicket'];
                    callback(uname, ticket);
                    Notification.success("Got profile.");
                }
            });
        } else {
            console.log("Getting username...1")
            console.log(state)
            state.fetch(profileId).then((profile) => {
                let profileObj = JSON.parse(JSON.stringify(profile));
                console.log(profileObj)
                Notification.success("Got profile.");
                uname = profileObj.preferred_username;
                ticket = profileObj.proxyGrantingTicket;
                callback(uname, ticket);
            }).catch((error) => {
                console.log("failed to get profile")
                console.log(error)
                callback(uname, ticket);
                Notification.error("Get profile failed. ", { autoClose: false });
            });
        }
    })


}*/


// Copies jupyter notebook command or product folder path to user clipboard 
export async function copyTextToClipboard(text: string, successMessage: string) {
    try {
        await navigator.clipboard.writeText(text).then(() => {Notification.success(successMessage, { autoClose: 3000 })})
    } catch (error) {
        console.warn('Copy failed', error)
    }
}


export const openSubmitJobs = (jupyterApp, data) => {
    if (jupyterApp.commands.hasCommand(JUPYTER_EXT.SUBMIT_JOBS_OPEN_COMMAND)) {
        if (data == null) {
            jupyterApp.commands.execute(JUPYTER_EXT.SUBMIT_JOBS_OPEN_COMMAND, null)
        }else {
            jupyterApp.commands.execute(JUPYTER_EXT.SUBMIT_JOBS_OPEN_COMMAND, data)
        }
    }
}

export const openViewJobs = (jupyterApp, data) => {
    if (jupyterApp.commands.hasCommand(JUPYTER_EXT.VIEW_JOBS_OPEN_COMMAND)) {
        if (data == null) {
            jupyterApp.commands.execute(JUPYTER_EXT.VIEW_JOBS_OPEN_COMMAND, null)
        }else {
            jupyterApp.commands.execute(JUPYTER_EXT.VIEW_JOBS_OPEN_COMMAND, data)
        }
    }
}