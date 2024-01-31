const axios = require('axios');
const fs = require('fs');
const path = require('path');

async function downloadFile(url, apiKey) {
  try {
    // 发送HTTP GET请求，带有身份验证的API_KEY
    const response = await axios.get(url, {
      headers: {
        'API-KEY': `${apiKey}`,
        KEY2: '123'
      },
      responseType: 'arraybuffer'
    });

    // 从URL中提取文件名
    const fileName = getFileNameFromUrl(url);

    // 将响应的二进制数据写入文件
    fs.writeFileSync(fileName, Buffer.from(response.data, 'binary'));

    console.log(`File downloaded successfully: ${fileName}`);
  } catch (error) {
    console.error('Error downloading file:', error.message);
  }
}

// 从URL中提取文件名的辅助函数
function getFileNameFromUrl(url) {
  const matches = url.match(/\/([^\/?#]+)[^\/]*$/);
  return matches && matches.length > 1 ? matches[1] : 'file';
}

// 使用例子
const url = 'http://127.0.0.1:8000/files/1.txt';
const apiKey = 'chrdw,hdhxt,szpzc,lljxk';

downloadFile(url, apiKey);
