function filterFiles(req, res, next) {
    if (!req.files) {
        res.status(400).send('Ни одного файла не было загружено')
        return
    }

    const count = Object.keys(req.files).length
    if (count != 1) {
        res.status(400).send('Было загружено неверное число файлов')
        return
    }

    const allowedTypes = ['application/zip']
    const file = req.files.file

    if (!allowedTypes.includes(file.mimetype)) {        
        res.status(400).send('Не тот формат файла')
        return
    }

    next()
}

module.exports = {
    filterFiles
}
