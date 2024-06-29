// /src/app/components/ProductInfoCard.jsx

export default function ProductInfoCard({ product, addToCart }) {
    return (
        <div className="flex flex-col space-y-3">
            <div className="bg-white rounded flex flex-col space-y-3">
                <div className="text-lg border p-2 border-gray-300">
                    {product ? product.name : '商品名が表示されます'}
                </div>
                <div className="text-lg border p-2 border-gray-300">
                    {product ? `${product.price}円` : '価格が表示されます'}
                </div>
            </div>
            <button
                onClick={addToCart}
                disabled={!product}
                className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 rounded w-full"
            >
                追加
            </button>
        </div>
    );
}
