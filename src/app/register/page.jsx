// /src/app/register/page.jsx

"use client";
import { useState } from 'react';
import ProductInfoCard from "src/app/components/ProductInfoCard";
import fetchProduct from "./fetchProduct";

export default function RegisterPage() {
    const [productCode, setProductCode] = useState('');
    const [product, setProduct] = useState(null);
    const [cart, setCart] = useState([]);

    const handleProductCodeSubmit = async () => {
        try {
            const productData = await fetchProduct(productCode);
            setProduct(productData);
        } catch (error) {
            console.error('商品のフェッチに失敗しました:', error);
            alert('商品がマスタ未登録です。');
        }
    };

    const addToCart = () => {
        if (!product) return;
        const newItem = { ...product, quantity: 1 };
        setCart([...cart, newItem]);
        setProduct(null);
        setProductCode('');
    };

    const handleCheckout = async () => {
        if (cart.length === 0) return;
        try {
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/checkout`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ items: cart }),
            });
            if (!response.ok) throw new Error('チェックアウトに失敗しました。');
            alert('購入が完了しました。');
            setCart([]);
        } catch (error) {
            console.error('チェックアウト処理エラー:', error);
            alert('購入に失敗しました。');
        }
    };

    return (
        <div className="flex justify-center items-center h-screen bg-gray-100">
            <div className="bg-white rounded-lg p-8 shadow-lg flex w-full max-w-4xl">
                <div className="w-1/2 pr-4">
                    <div className="mb-4">
                        <input
                            className="border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
                            type="text"
                            value={productCode}
                            onChange={(e) => setProductCode(e.target.value)}
                            placeholder="商品コードを入力"
                            onKeyPress={(e) => e.key === 'Enter' && handleProductCodeSubmit()}
                        />
                        <button
                            onClick={handleProductCodeSubmit}
                            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded w-full mt-3"
                        >
                            商品コード読み込み
                        </button>
                    </div>
                    <ProductInfoCard product={product} addToCart={addToCart} />
                </div>
                <div className="w-1/2 pl-4">
                    <div className="text-xl text-center text-gray-500 p-3 ">
                        購入リスト
                    </div>
                    <ul className="bg-white border p-4 h-64 overflow-y-auto">
                        {cart.map((item, index) => (
                            <li key={index} className="flex justify-between items-center py-2 border-b">
                                <span>
                                    {item.name} x {item.quantity} @ {item.price}円
                                    {" - 税抜き合計: "}{item.quantity * item.price}円
                                </span>
                            </li>
                        ))}
                        {cart.length === 0 && (
                            <li className="text-center text-gray-500">カートは空です。</li>
                        )}
                    </ul>
                    <button
                        onClick={handleCheckout}
                        disabled={cart.length === 0}
                        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded w-full mt-4"
                    >
                        購入
                    </button>
                </div>
            </div>
        </div>
    );
}