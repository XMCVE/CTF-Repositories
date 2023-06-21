function mergeObjects(targetObj, sourceObj, valueToMerge) {
    for (const key in sourceObj) {
        if (typeof sourceObj[key] === 'object' && sourceObj[key] !== null) {
            targetObj[key] = targetObj[key] || {};
            mergeObjects(targetObj[key], sourceObj[key], valueToMerge);
        } else if (sourceObj[key] === valueToMerge) {
            targetObj[key] = sourceObj[key];
        }
    }
}

function merge(obj,key,value) {
    const dotIndex = key.indexOf(".");
    if (dotIndex != -1){
        const key1 = key.substring(0, dotIndex);
        const key2 = key.substring(dotIndex + 1);
        merge(obj[key1],key2,value)
    }else {
        obj[key] = value
    }
}
function checkValue (obj, value) {
    for (const key in obj ) {
        if (typeof obj[key] === 'object') {
            if (checkValue(obj[key], value)) {
                return true;
            }
        } else if (obj[key] === value) {
            return true;
        }
    }
    return false;
};
module.exports = {
    mergeObjects,
    merge,
    checkValue,
};
