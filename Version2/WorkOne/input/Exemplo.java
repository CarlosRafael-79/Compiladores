public class Exemplo {
    public static void main ( String [ ] args ){
        double a, b;
        a = lerDouble();
        b = 5;
        if(a > b){
            System.out.println(a);
        }else{
            System.out.println(b);
        }

        while(a>0){
            System.out.println(a);
            a = a - 1;
        }
    }
}