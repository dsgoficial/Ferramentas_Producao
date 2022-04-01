import concurrent.futures
import os
import json

class Filters:
    
    def filterCommonFields(self, selectedLayers):
        commonFields = []
        if len(selectedLayers) == 1:
            return [
                [n, 1]
                for n in selectedLayers[0].fields().names()
            ]
        else:
            fieldLists = []
            for l in selectedLayers:
                fieldNames = l.fields().names()
                fieldLists.append(fieldNames)
            commonFields = list(set(fieldLists[0]).intersection(*fieldLists[1:]))  
            return [ [n] for n in commonFields]

    def filterAttributeCombination(self, selectedFields, selectedLayers):
        attributeLists = []
        def readAttributes(f):
            values = []
            for fieldName in selectedFields:
                values.append(f[fieldName])
            attributeLists.append(values)
        
        pool = concurrent.futures.ThreadPoolExecutor(os.cpu_count()-1)
        futures = set()
        for layer in selectedLayers:
            features = list(layer.getFeatures())
            for feature in features:
                futures.add(pool.submit(readAttributes, feature))
        concurrent.futures.wait(futures, timeout=None, return_when=concurrent.futures.ALL_COMPLETED)
        attributeCountMap = {
            ','.join([str(n) for n in attributes]): attributeLists.count(attributes) 
            for attributes in attributeLists
        }
        rows = []
        for key in attributeCountMap:
            displayValues = []
            dump = {}
            attributes = key.split(',')
            for idx, attribute in enumerate(attributes):
                dump[selectedFields[idx]] = attribute
                displayValues.append('{} ({})'.format(attribute, selectedFields[idx]))
            rows.append(
                [
                    ';\n'.join(displayValues),
                    attributeCountMap[key],
                    json.dumps(dump)
                ]
            )
        return rows

    def getLayersByAttributes(self, selectedAttributes, selectedLayers):
        filterExpression = self.getFilterExpression(selectedAttributes)
        rows = []
        for layer in selectedLayers:
            layer.selectByExpression(filterExpression)
            count = layer.selectedFeatureCount()
            if count == 0:
                continue
            rows.append(
                [
                    layer.name(),
                    count
                ]
            )
        return rows

    def getFilterExpression(self, fieldLists):
        allExpressions = []
        for fields in fieldLists:
            expressions = []
            for n in fields:
                expressions.append(
                    '"{}" is {}'.format(
                        n,
                        self.formatValue(fields[n]) 
                    )
                )
            allExpressions.append(' AND '.join(expressions))
        return ' AND '.join(allExpressions) 

    def formatValue(self, value):
        if self.isNumber(value):
            return value
        if value == 'NULL':
            return value
        return "'{}'".format(value)

    def isNumber(self, value):
        for t in [int, float]:
            try:
                t(value)
            except:
                return False
        return True