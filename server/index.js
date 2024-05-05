const fs = require('fs')
const path = require('path')
const { filterFiles } = require('./middleware.js')
const { generateKey, checkZipContentFromRequest, saveFileFromRequest } = require('./utility.js')

const fileUpload = require('express-fileupload')
const express = require('express')

const app = express()
const PORT = 3000

app.use(fileUpload())

app.get('/', (req, res) => {
    const key = req.query.key
    if (!key) {
        res.sendStatus(400)
        return
    }

    const filePath = path.resolve('files', `${key}.zip`)
    fs.existsSync(filePath) ? res.download(filePath) : res.sendStatus(404)
})

app.post('/', filterFiles, (req, res) => {
    const key = req.query.key
    const files = fs.readdirSync('files')
    
    if (!key) {
        let newKey = generateKey()
        while (files.includes(newKey))
            newKey = generateKey()

        if (checkZipContentFromRequest(req)) {
            saveFileFromRequest(req, newKey)
            res.json({ 'key': newKey })
        }
        else {            
            res.sendStatus(415)
        }
    }
    else if (files.includes(key)) {
        if (checkZipContentFromRequest(req)) {
            saveFileFromRequest(req, key)
            res.sendStatus(202)
        }
        else {
            res.sendStatus(415)
        }
    }
    else {
        res.sendStatus(404)
    }
})

app.listen(PORT, () => {
    console.log(`App listening on port ${PORT}`)
})
