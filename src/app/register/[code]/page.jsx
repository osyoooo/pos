// /src/app/register/[code]/page.jsx
// このコードは実際は利用されていない

"use client";
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import fetchProduct from "../fetchProduct";

export default function ProductPage() {
	const router = useRouter();
	const { code } = router.query;
	const [product, setProduct] = useState(null);

	useEffect(() => {
		const fetchAndSetProduct = async () => {
			try {
				const productData = await fetchProduct(code);
				setProduct(productData);
			} catch (error) {
				console.error('Error fetching product:', error);
				alert('商品がマスタ未登録です');
			}
		};

		if (code) {
			fetchAndSetProduct();
		}
	}, [code]);

	return (
		<>
			{product && (
				<div>
					<h1>{product.name}</h1>
					<p>価格: ¥{product.price}</p>
					<p>商品コード: {product.code}</p>
				</div>
			)}
		</>
	);
}
