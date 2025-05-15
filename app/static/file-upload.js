const baseURL = `${window.location.protocol}//${window.location.hostname}:5000`;

const uploadClick = (event) => {
    merchantSelectEle = document.getElementById('merchantSelect')
    fileUploadEle = document.getElementById('fileUpload')
    
    if(merchantSelectEle?.value && fileUploadEle?.files?.length == 1) {
        const file = fileUploadEle?.files[0];
        const formData = new FormData();
        formData.append("file", file);
        formData.append("merchant_id", parseInt(merchantSelectEle.value)); 

        fetch(`${baseURL}/api/upload_csv`, {
                method: "POST",
                body: formData
        }).then((response) => {
            response.json().then((json) => {
                const myModalEl = document.getElementById('uploadModal');
                if (myModalEl) {
                    const modal = bootstrap.Modal.getInstance(myModalEl);
                    modal.hide()
                    displayToastMessage([json.message]);
                }
            })
        }).catch((e) => {
            console.log(e)
        })
    }
}
const onLoadCSV = (event) => {
    const file = event.target.files[0];
    const buttonContainer = document.getElementById('uploadButtonContainer');
    const tableContainer = document.getElementById('uploadTableContainer');

    if (file) {
        // Only insert if not already there
        if (!document.getElementById('dynamicUploadBtn')) {
            buttonContainer.innerHTML = `
                <button id="dynamicUploadBtn" class="btn btn-primary mt-2" onclick="uploadClick(event)">
                    Upload
                </button>
            `;
        }
        document.getElementById('uploadTextDescription').innerHTML = `You've uploaded ${file.name}. Want to replace it? Click here to browse again`;
        loadDynamicTable(file, tableContainer)
    } else {
        // Clear the button if no file is selected
        buttonContainer.innerHTML = '';
        tableContainer.innerHTML = '';
        document.getElementById('uploadTextDescription').innerHTML =
            'Drop your CSV file here, or click to browse for it.';
        
    }
}


const loadDynamicTable = (file, element) => {
    readAndGetData(file).then(({csvheader, csvbody}) => {
        addProductName(csvheader, csvbody).then(({header, body}) => {
            const innerHTML = `
    <div class="table-responsive">
        <table class="table table-hover">
            <thead>
                <tr>
                    ${header.map(item => '<th scope="col">' + item + '</th>').join('')}
                </tr>
            </thead>
            <tbody>
                ${
                    body.map(row => ['<tr>', row.map((value, index) => {
                            if(index === 0) {
                                return [`<td class="${value.isExists ? "text-success" : "text-warning"}">`, value.value, "</td>"].join("")
                            } else {
                                return ["<td>",value, "</td>"].join("")
                            }
                        }).join("")
                    ,'</tr>'].join("")).join("")
                }
            
            </tbody>
        </table>
    </div>
    `
    element.innerHTML = innerHTML
        })
    })
}

const addProductName = async (header, body) => {
    header.unshift("Product Name");

    const promiseList = body.map(async (item) => {
        try {
            const res = await fetch(`${baseURL}/api/product/exists/${item[0]}`);
            const data = await res.json();

            if (data?.exists && data?.product?.name) {
                item.unshift({value: data.product.name, isExists: true});
            } else {
                item.unshift({value: "Product not found!", isExists: false});
            }
            return item;
        } catch (err) {
            item.unshift({value: "Error fetching product", isExists: false});
            return item;
        }
    });

    const updatedBody = await Promise.all(promiseList);
    return { header, body: updatedBody };
};


const readAndGetData = (file) => {
    return new Promise((resolve, reject) => {
        const header = []; 
        const data = [];
        const reader = new FileReader();

        reader.onload = function(e) {
            const content = e.target.result;
            const rows = content.trim().split('\n');

            rows.forEach((row, index) => {
                const values = row.split(',');
                if (index === 0) {
                    header.push(...values);
                } else {
                    data.push(values);
                }
            });

            resolve({ csvheader: header, csvbody: data });
        };

        reader.onerror = () => reject(reader.error);

        if (file) {
            reader.readAsText(file);
        } else {
            reject(new Error('No file provided'));
        }
    });
}