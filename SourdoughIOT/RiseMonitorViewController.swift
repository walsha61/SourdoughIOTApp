//
//  RiseMonitorViewController.swift
//  SourdoughIOT
//
//  Created by Anneliese Walsh on 12/03/2022.
//  Copyright © 2022 Anneliese Walsh. All rights reserved.
//

import UIKit
import TinyConstraints
import Charts

//
//var dictJson:[String:Any] = [:]
//init() {
//    self.dictJson = Dictionary<String,Any>()
//}
//
//required init?(coder: NSCoder) {
//    fatalError("init(coder:) has not been implemented")
//}

class RiseMonitorViewController: UIViewController, ChartViewDelegate {
    var dictJson:[String:Any] = [:]
//    init() {
//        self.dictJson = Dictionary<String,Any>()
//    }

//    required init?(coder: NSCoder) {
//        fatalError("init(coder:) has not been implemented")
//    }
    

    lazy var lineChartView: LineChartView = {
        let chartView = LineChartView()
        
        chartView.rightAxis.enabled = false
        
        // Customise the y axis
        let yAxis = chartView.leftAxis
        yAxis.labelFont = .boldSystemFont(ofSize: 12)
        yAxis.setLabelCount(6, force: false)
        yAxis.labelTextColor = .black
        yAxis.axisLineColor = .black
        
        // Customise the x axis
        chartView.xAxis.labelPosition = .bottom
        chartView.xAxis.labelFont = .boldSystemFont(ofSize: 12)
        chartView.xAxis.setLabelCount(6, force: false)
        chartView.xAxis.axisLineColor = .systemBlue

        return chartView
    }()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        

        // Do any additional setup after loading the view.
        
        view.addSubview(lineChartView)
        lineChartView.centerInSuperview()
        lineChartView.width(to: view)
        lineChartView.heightToWidth(of: view)
        
        NotificationCenter.default.addObserver(self, selector: #selector(setData), name: Notification.Name("NewFunctionName"), object: nil)
    
        //setData()
        //var dictJson:[String:String] = [:]
//        var isDictEmpty = dictJson.count == 0
//        print("isDictEmpty: \(isDictEmpty)")
//        setData()

//        if (isDictEmpty == false) {
//            setData()
//        }
    }
    
    func chartValueSelected(_ chartView: ChartViewBase, entry: ChartDataEntry, highlight: Highlight) {
        print(entry)
    }
    
    @objc func setData(notification: NSNotification) {
        
        guard let yVal = notification.object as? [ChartDataEntry]  else {
                    return
                }
//        var pageController  = ViewController()
//        var yVal = pageController.yValues
        print("Setting yvalues", yVal)
        
        let set1 = LineChartDataSet(entries: yVal, label: "Rise")
        
        // Customise the set1 line
        set1.mode = .cubicBezier
        set1.drawCirclesEnabled = false
        set1.lineWidth = 2
        set1.setColor(.blue)
        set1.fillAlpha = 0.8

        
        let data = LineChartData(dataSet: set1)
        data.setDrawValues(false)
        lineChartView.data = data
    }
    
    // Need to replace these with incoming JSON data (segue?)

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    */

}
