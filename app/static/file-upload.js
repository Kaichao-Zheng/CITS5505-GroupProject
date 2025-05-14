const uploadClick = (event) => {
    merchantSelectEle = document.getElementById('merchantSelect')
    fileUploadEle = document.getElementById('fileUpload')

    const baseURL = `${window.location.protocol}//${window.location.hostname}:5000`;

    if(merchantSelectEle?.value && fileUploadEle?.files?.length == 1) {
        const file = fileUploadEle?.files[0];
        const formData = new FormData();
        formData.append("file", file);

        fetch(`${baseURL}/api/upload_csv`,
            {
                method: "POST",
                body: formData
            }
        ).then((response) => {
            response.json().then((json) => {
                console.log(json);
            })
        }).catch((e) => {
            console.log(e)
        })
    }
}