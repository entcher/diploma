const path = require('path')
const AdmZip = require('adm-zip')

function checkZipContentFromRequest(req) {
	const zip = new AdmZip(req.files.file.data)
	const zipEntries = zip.getEntries()
	if (zipEntries.length > 2)
		return false

	const allowedExtensions = ['json', 'csv']
	for (entry of zipEntries) {
		const extension = entry.entryName.split('.').pop()
		if (!allowedExtensions.includes(extension)) {
			return false
		}
	}
	return true
}

function saveFileFromRequest(req, key) {
	const uploadedFile = req.files.file
	const uploadPath = path.resolve('files', `${key}.zip`)
	uploadedFile.mv(uploadPath)
}

module.exports = {
	checkZipContentFromRequest,
	saveFileFromRequest
}