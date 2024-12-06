const _parseAlgoInputs = (body: any) => {
    body = JSON.parse(body)
    let inputs: any[] = body["wps:ProcessOfferings"]["wps:ProcessOffering"]["wps:Process"]["wps:Input"]
    return inputs
}


const _parseAlgoDesc = (body: any) => {
    body = JSON.parse(body)
    let description: String = body["wps:ProcessOfferings"]["wps:ProcessOffering"]["wps:Process"]["ows:Title"]
    return description
}

export const getAlgorithmMetadata = (body: any) => {
    let algorithmMetadata = {
        description: '',
        inputs: {}
    }

    //algorithmMetadata.description = _parseAlgoDesc(body)
    algorithmMetadata.inputs = _parseAlgoInputs(body)

    return algorithmMetadata
}

export const parseScienceKeywords = (keywords: any) => {
    var scienceKeywords: string[] = []
    _getAllValues(keywords, scienceKeywords)
    return scienceKeywords
}


const _getAllValues = (keywords: any, scienceKeywords : string[]) => {
    for (let k in keywords) {
        if (typeof keywords[k] === "object") {
            _getAllValues(keywords[k], scienceKeywords)
        } else {
            if (!scienceKeywords.includes(keywords[k]))
                scienceKeywords.push(keywords[k])
        }
    }
}

export const delay = ms => new Promise(res => setTimeout(res, ms));