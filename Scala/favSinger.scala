object favSinger{
    def main(args: Array[String])={
        val N = "5"
        val a = "1 1 2 2 4"
        val arr: Array[String] = a.split(",")
        var total = 0
        println(arr.length)
        for (i <- 0 until arr.length){
            for (j <- i+1 until arr.length){
                println(arr(i), arr(j))
                if (arr(i) == arr(j)){
                    total = total + 1
                }
            }

        }
    }
}