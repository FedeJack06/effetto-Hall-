{

    double_t V , v , B , b , EV , ev , EB , eb;
    double V_hall , V_long;
    int i=0;
    string fileName = "file_con_B+"
    string filename = "file_con_B-"

    ifstream input1(fileName);
    ifstream input2(filename);


    ofstream out1("vhall.dat");
    ofstream out2("vlong.dat");

/*
    TLatex t1, t2;
    string title1 = t1.DrawLatex(0.5 , .6 ,"tensione di hall vs campo magnetico")
    string title2 = t2.DrawLatex(0. , .6 ,"V_long vs campo magnetico")
*/

    auto *c1 = new TCanvas( "c1" , "tensione di hall vs campo magnetico") 
    auto *c1 = new TCanvas( "c1" , "V_long vs campo magnetico") 

    auto *vhall  = new TGraphErrors;
    auto *vlong  = new TGraphErrors;


    const char *function1 = "[0] + [1]*x"
    const char *function2 = "[2] + [3]*pow(x,2)"


    auto *f1 = new TF1("f1", function1)
    auto *f2 = new TF1("f2", function2)


    while (input1 >> V >> B >> EV >> EB) // maiuscole B+ , minuscole B-
    {
        intput2 >> v >> b >> ev >> eb

        V_hall = (V-v)/2
        V_long = (V+v)/2

        ev_both = sqrt(pow(EV,2)+pow(ev,2))

        out1 << V_hall << B << ev_both << EB
        out2 << V_long << B << ev_both << EB


        vhall->SetPoint(i, B , V_hall)
        vlong->SetPoint(i, B , V_long)

        vhall->SetPointError(i, EB , ev_both)
        vlong->SetPointError(i, EB , ev_both)

        i++
        
    }
    



    vhall->Draw("AP")
    vlong->Draw("AP")

    vhall->Fit("f1")
    vlong->Fit("f2")








}