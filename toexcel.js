let data =require(`./openfacilities.json`)
const XLSX = require(`xlsx`);
const ws = XLSX.utils.json_to_sheet(data)
const wb = XLSX.utils.book_new()

XLSX.utils.book_append_sheet(wb, ws, 'Responses')
XLSX.writeFile(wb, 'openfacilities.xlsx')
