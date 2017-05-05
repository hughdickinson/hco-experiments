db.classifications.aggregate([
    {
        $group:{
            _id:'$subject_id',
            real:{$sum:{$cond:[{$eq:['$annotation',1]},1,0]}},
            bogus:{$sum:{$cond:[{$eq:['$annotation',0]},1,0]}}
        }
    },
    {
        $project:{
            _id:1,real:1,bogus:1,controv:{
                $cond:[
                    {$gt:['$real','$bogus']},
                    {$pow:[{$add:['$real','$bogus']},{$divide:['$bogus','$real']}]},
                    {$pow:[{$add:['$real','$bogus']},{$divide:['$real','$bogus']}]}
                ]
            }
        }
    },
    {
        $sort:{
            controv:-1
        }
    }
])
