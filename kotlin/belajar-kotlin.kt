import java.util.*

fun main() {
    print("Enter flag: ")
    val input = readLine() ?: ""
    
    if (isValidFlag(input)) {
        println("🎉 Access granted! Flag accepted.")
    } else {
        println("🚫 Access denied.")    
    }
}

fun isValidFlag(flag: String): Boolean {
    if (flag.length != 24) return false
    if (!flag.startsWith("W92{") || !flag.endsWith("}")) return false

    val inner = flag.substring(4, 23)
    val secret = "r3v_k0tlin_4_th3_win"
    
    return inner == xorWithKey(secret, "W92")
}

fun xorWithKey(input: String, key: String): String {
    return input.mapIndexed { i, c ->
        (c.code xor key[i % key.length].code).toChar()
    }.joinToString("")
}