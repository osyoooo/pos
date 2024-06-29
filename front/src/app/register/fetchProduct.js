// src/app/register/fetchProduct.js

export default async function fetchProduct(code) {
    const url = `${process.env.NEXT_PUBLIC_API_ENDPOINT}products/code/${code}`;
    const response = await fetch(url, {
        method: 'GET', // GETメソッドを指定
        headers: {
            'Content-Type': 'application/json'
        }
    });

    if (!response.ok) {
        throw new Error('製品データの取得に失敗しました');
    }
    return await response.json();
}
