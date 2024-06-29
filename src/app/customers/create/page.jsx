"use client"
import { useRef } from 'react';
import { useRouter } from 'next/navigation';

import createCustomer from './createCustomer';

export default function CreatePage() {
    const formRef = useRef();
    const router = useRouter();

    const handleSubmit = async (event) => {
        event.preventDefault();
        const formData = new FormData(formRef.current);

        // customer_id の値を取得
        const customerID = formData.get("customer_id");

        // customer_id が空白の場合はエラーメッセージを表示して処理を中断
        if (!customerID.trim()) {
            alert("CustomerIDを入力してください");
            return; // これ以上の処理を行わない
        }

        await createCustomer(formData);
        router.push(`./create/confirm?customer_id=${customerID}`);
    };

    return (
        <>
            <div className="card bordered bg-white border-blue-200 border-2 max-w-md m-4">
                <div className="m-4 card bordered bg-blue-200 duration-200 hover:border-r-red">
                    <form ref={formRef} onSubmit={handleSubmit}>
                        <div className="card-body">
                            <h2 className="card-title">
                                <p><input type="text" name="customer_name" placeholder="桃太郎" className="input input-bordered" /></p>
                            </h2>
                            <p>Customer ID:<input type="text" name="customer_id" placeholder="C030" className="input input-bordered" required /></p>
                            <p>Age:<input type="number" name="age" placeholder="30" className="input input-bordered" /></p>
                            <p>Gender:<input type="text" name="gender" placeholder="女" className="input input-bordered" /></p>
                        </div>
                        <div className="flex justify-center">
                            <button type="submit" className="btn btn-primary m-4 text-2xl">
                                作成
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </>
    )
}
