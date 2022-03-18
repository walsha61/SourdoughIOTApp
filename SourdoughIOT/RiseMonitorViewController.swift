//
//  RiseMonitorViewController.swift
//  SourdoughIOT
//
//  Created by Anneliese Walsh on 12/03/2022.
//  Copyright © 2022 Anneliese Walsh. All rights reserved.
//

import UIKit
import Charts
import TinyConstraints

class RiseMonitorViewController: UIViewController, ChartViewDelegate {

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
    
        setData()
    }
    
    func chartValueSelected(_ chartView: ChartViewBase, entry: ChartDataEntry, highlight: Highlight) {
        print(entry)
    }
    
    func setData() {
        let set1 = LineChartDataSet(entries: yValues, label: "Rise")
        
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
    let yValues: [ChartDataEntry] = [
        ChartDataEntry(x: 0.0, y: 10.0),
        ChartDataEntry(x: 1.0, y: 15.0),
        ChartDataEntry(x: 2.0, y: 20.0),
        ChartDataEntry(x: 3.0, y: 25.0),
        ChartDataEntry(x: 4.0, y: 30.0)
    ]

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    */

}
